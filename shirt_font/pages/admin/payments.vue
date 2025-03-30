<template>
    <AdminLayout>
        <div class="payments-management">
            <div class="page-header">
                <h1>จัดการการชำระเงิน</h1>
            </div>

            <div class="stats-cards">
                <div class="stat-card">
                    <div class="stat-icon pending">⌛</div>
                    <div class="stat-content">
                        <h3>รอตรวจสอบ</h3>
                        <div class="stat-value">{{ stats.pending }}</div>
                        <div class="stat-text">รายการ</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon approved">✓</div>
                    <div class="stat-content">
                        <h3>อนุมัติแล้ว</h3>
                        <div class="stat-value">{{ stats.approved }}</div>
                        <div class="stat-text">รายการ</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon rejected">✗</div>
                    <div class="stat-content">
                        <h3>ปฏิเสธ</h3>
                        <div class="stat-value">{{ stats.rejected }}</div>
                        <div class="stat-text">รายการ</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon total">💰</div>
                    <div class="stat-content">
                        <h3>ยอดรวมวันนี้</h3>
                        <div class="stat-value">฿{{ formatNumber(stats.todayAmount) }}</div>
                        <div class="stat-text">บาท</div>
                    </div>
                </div>
            </div>

            <div class="filter-section">
                <div class="search-box">
                    <input type="text" v-model="searchQuery" placeholder="ค้นหาเลขคำสั่งซื้อหรือชื่อลูกค้า..." />
                </div>
                <div class="filter-box">
                    <select v-model="statusFilter">
                        <option value="">ทุกสถานะ</option>
                        <option value="pending">รอตรวจสอบ</option>
                        <option value="approved">อนุมัติแล้ว</option>
                        <option value="rejected">ปฏิเสธ</option>
                    </select>
                    <select v-model="paymentMethodFilter">
                        <option value="">ทุกช่องทาง</option>
                        <option value="bank_transfer">โอนผ่านธนาคาร</option>
                        <option value="credit_card">บัตรเครดิต</option>
                        <option value="promptpay">พร้อมเพย์</option>
                    </select>
                    <select v-model="dateFilter">
                        <option value="">ทุกช่วงเวลา</option>
                        <option value="today">วันนี้</option>
                        <option value="yesterday">เมื่อวาน</option>
                        <option value="week">7 วันล่าสุด</option>
                        <option value="month">30 วันล่าสุด</option>
                    </select>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <p>{{ error }}</p>
                <button @click="fetchPayments" class="retry-button">ลองใหม่</button>
            </div>

            <div v-else class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>เลขอ้างอิง</th>
                            <th>เลขที่คำสั่งซื้อ</th>
                            <th>ลูกค้า</th>
                            <th>จำนวนเงิน</th>
                            <th>วิธีชำระเงิน</th>
                            <th>วันที่ชำระ</th>
                            <th>สถานะ</th>
                            <th>การจัดการ</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="payment in filteredPayments" :key="payment.id">
                            <td>{{ payment.reference_id }}</td>
                            <td>{{ payment.order_number }}</td>
                            <td>{{ payment.customer_name }}</td>
                            <td>฿{{ formatNumber(payment.amount) }}</td>
                            <td>{{ getPaymentMethodName(payment.payment_method) }}</td>
                            <td>{{ formatDate(payment.payment_date) }}</td>
                            <td>
                                <span class="status-badge" :class="payment.status">
                                    {{ getStatusName(payment.status) }}
                                </span>
                            </td>
                            <td class="actions">
                                <button class="view-btn" @click="viewPayment(payment)">ดูรายละเอียด</button>
                                <button class="approve-btn" @click="confirmApprovePayment(payment)"
                                    v-if="payment.status === 'pending'">อนุมัติ</button>
                                <button class="reject-btn" @click="confirmRejectPayment(payment)"
                                    v-if="payment.status === 'pending'">ปฏิเสธ</button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div v-if="filteredPayments.length === 0" class="empty-state">
                    <p>ไม่พบข้อมูลการชำระเงินที่ตรงกับเงื่อนไขการค้นหา</p>
                </div>

                <div class="pagination" v-if="totalPages > 1">
                    <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">&laquo; ก่อนหน้า</button>
                    <span>หน้า {{ currentPage }} จาก {{ totalPages }}</span>
                    <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">ถัดไป
                        &raquo;</button>
                </div>
            </div>
        </div>

        <!-- Payment Details Modal -->
        <div v-if="showDetailsModal" class="modal-overlay">
            <div class="modal-content payment-details-modal">
                <div class="modal-header">
                    <h2>รายละเอียดการชำระเงิน</h2>
                    <button class="close-button" @click="showDetailsModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="payment-details">
                        <div class="payment-info-section">
                            <h3>ข้อมูลการชำระเงิน</h3>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="label">เลขอ้างอิง:</span>
                                    <span>{{ selectedPayment.reference_id }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">เลขที่คำสั่งซื้อ:</span>
                                    <span>{{ selectedPayment.order_number }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">ยอดชำระ:</span>
                                    <span class="amount">฿{{ formatNumber(selectedPayment.amount) }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">วิธีชำระเงิน:</span>
                                    <span>{{ getPaymentMethodName(selectedPayment.payment_method) }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">วันที่ชำระ:</span>
                                    <span>{{ formatDateTime(selectedPayment.payment_date) }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">สถานะ:</span>
                                    <span class="status-badge" :class="selectedPayment.status">
                                        {{ getStatusName(selectedPayment.status) }}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div class="payment-info-section">
                            <h3>ข้อมูลลูกค้า</h3>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="label">ชื่อ:</span>
                                    <span>{{ selectedPayment.customer_name }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">อีเมล:</span>
                                    <span>{{ selectedPayment.customer_email }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">เบอร์โทรศัพท์:</span>
                                    <span>{{ selectedPayment.customer_phone }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="payment-info-section" v-if="isBankTransfer || isPromptpay">
                            <h3>รายละเอียดการโอน</h3>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="label">โอนเข้าธนาคาร:</span>
                                    <span>{{ selectedPayment.payment_details?.bank_name || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">เลขที่บัญชี:</span>
                                    <span>{{ selectedPayment.payment_details?.account_number || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">ชื่อบัญชี:</span>
                                    <span>{{ selectedPayment.payment_details?.account_name || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">โอนจากธนาคาร:</span>
                                    <span>{{ selectedPayment.payment_details?.from_bank || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">เวลาโอน:</span>
                                    <span>{{ formatDateTime(selectedPayment.payment_details?.transfer_time) || '-' }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="payment-info-section" v-if="isCreditCard">
                            <h3>ข้อมูลบัตร</h3>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="label">เลขบัตร:</span>
                                    <span>{{ maskCardNumber(selectedPayment.payment_details?.card_number) || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">ประเภท:</span>
                                    <span>{{ selectedPayment.payment_details?.card_type || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">รหัสอนุมัติ:</span>
                                    <span>{{ selectedPayment.payment_details?.approval_code || '-' }}</span>
                                </div>
                            </div>
                        </div>

                        <div class="payment-info-section" v-if="isBankTransfer || isPromptpay">
                            <h3>หลักฐานการชำระเงิน</h3>
                            <div class="payment-evidence">
                                <img v-if="selectedPayment.payment_details?.receipt_image"
                                    :src="selectedPayment.payment_details.receipt_image" alt="หลักฐานการชำระเงิน"
                                    @click="openImagePreview(selectedPayment.payment_details.receipt_image)">
                                <div v-else class="no-evidence">ไม่มีหลักฐานการชำระเงิน</div>
                            </div>
                        </div>

                        <div class="payment-info-section" v-if="selectedPayment.status !== 'pending'">
                            <h3>ข้อมูลการตรวจสอบ</h3>
                            <div class="info-grid">
                                <div class="info-item">
                                    <span class="label">ตรวจสอบโดย:</span>
                                    <span>{{ selectedPayment.verified_by || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">เวลาที่ตรวจสอบ:</span>
                                    <span>{{ formatDateTime(selectedPayment.verified_at) || '-' }}</span>
                                </div>
                                <div class="info-item">
                                    <span class="label">หมายเหตุ:</span>
                                    <span>{{ selectedPayment.verified_note || '-' }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="regular-button" @click="showDetailsModal = false">ปิด</button>
                    <button class="approve-button" @click="confirmApprovePayment(selectedPayment)"
                        v-if="selectedPayment.status === 'pending'">อนุมัติการชำระเงิน</button>
                    <button class="reject-button" @click="confirmRejectPayment(selectedPayment)"
                        v-if="selectedPayment.status === 'pending'">ปฏิเสธการชำระเงิน</button>
                    <button class="print-button" @click="printPaymentDetails">พิมพ์</button>
                </div>
            </div>
        </div>

        <!-- Approve Payment Modal -->
        <div v-if="showApproveModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>อนุมัติการชำระเงิน</h2>
                    <button class="close-button" @click="showApproveModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <p>คุณต้องการอนุมัติการชำระเงินของคำสั่งซื้อ <strong>{{ paymentToApprove.order_number }}</strong>
                        ใช่หรือไม่?</p>
                    <div class="payment-summary">
                        <div class="summary-item">
                            <span class="label">เลขอ้างอิง:</span>
                            <span>{{ paymentToApprove.reference_id }}</span>
                        </div>
                        <div class="summary-item">
                            <span class="label">ลูกค้า:</span>
                            <span>{{ paymentToApprove.customer_name }}</span>
                        </div>
                        <div class="summary-item">
                            <span class="label">จำนวนเงิน:</span>
                            <span class="amount">฿{{ formatNumber(paymentToApprove.amount) }}</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="approveNote">หมายเหตุ (ถ้ามี)</label>
                        <textarea id="approveNote" v-model="approveNote" rows="3"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="showApproveModal = false">ยกเลิก</button>
                    <button class="approve-button" @click="approvePayment">ยืนยันการอนุมัติ</button>
                </div>
            </div>
        </div>

        <!-- Reject Payment Modal -->
        <div v-if="showRejectModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>ปฏิเสธการชำระเงิน</h2>
                    <button class="close-button" @click="showRejectModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <p>คุณต้องการปฏิเสธการชำระเงินของคำสั่งซื้อ <strong>{{ paymentToReject.order_number }}</strong>
                        ใช่หรือไม่?</p>
                    <div class="payment-summary">
                        <div class="summary-item">
                            <span class="label">เลขอ้างอิง:</span>
                            <span>{{ paymentToReject.reference_id }}</span>
                        </div>
                        <div class="summary-item">
                            <span class="label">ลูกค้า:</span>
                            <span>{{ paymentToReject.customer_name }}</span>
                        </div>
                        <div class="summary-item">
                            <span class="label">จำนวนเงิน:</span>
                            <span class="amount">฿{{ formatNumber(paymentToReject.amount) }}</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="rejectReason">เหตุผลในการปฏิเสธ <span class="required">*</span></label>
                        <textarea id="rejectReason" v-model="rejectReason" rows="3" required></textarea>
                        <div class="error-message" v-if="rejectReasonError">{{ rejectReasonError }}</div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="showRejectModal = false">ยกเลิก</button>
                    <button class="reject-button" @click="rejectPayment">ยืนยันการปฏิเสธ</button>
                </div>
            </div>
        </div>

        <!-- Image Preview Modal -->
        <div v-if="showImagePreview" class="modal-overlay" @click="showImagePreview = false">
            <div class="image-preview-container" @click.stop>
                <img :src="previewImageUrl" alt="หลักฐานการชำระเงิน">
                <button class="close-button" @click="showImagePreview = false">&times;</button>
            </div>
        </div>
    </AdminLayout>
</template>

<script>
import AdminLayout from '~/components/admin/AdminLayout.vue';
import usePayment from '~/composables/usePayment';

export default {
    components: {
        AdminLayout
    },
    setup() {
        const {
            payments,
            loading,
            error,
            stats,
            fetchAllPayments,
            updatePaymentStatus
        } = usePayment();

        return {
            payments,
            loading,
            error,
            stats,
            fetchAllPayments,
            updatePaymentStatus
        };
    },
    data() {
        return {
            searchQuery: '',
            statusFilter: '',
            paymentMethodFilter: '',
            dateFilter: '',
            currentPage: 1,
            itemsPerPage: 10,
            showDetailsModal: false,
            showApproveModal: false,
            showRejectModal: false,
            showImagePreview: false,
            selectedPayment: {},
            paymentToApprove: {},
            paymentToReject: {},
            approveNote: '',
            rejectReason: '',
            rejectReasonError: '',
            previewImageUrl: '',
        };
    },
    computed: {
        filteredPayments() {
            let result = this.payments;

            // Apply search filter
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                result = result.filter(payment =>
                    payment.reference_id.toLowerCase().includes(query) ||
                    payment.order_number.toLowerCase().includes(query) ||
                    payment.customer_name.toLowerCase().includes(query)
                );
            }

            // Apply status filter
            if (this.statusFilter) {
                result = result.filter(payment => payment.status === this.statusFilter);
            }

            // Apply payment method filter
            if (this.paymentMethodFilter) {
                result = result.filter(payment => payment.payment_method === this.paymentMethodFilter);
            }

            // Apply date filter
            if (this.dateFilter) {
                const today = new Date();
                today.setHours(0, 0, 0, 0);

                const yesterday = new Date(today);
                yesterday.setDate(yesterday.getDate() - 1);

                const weekAgo = new Date(today);
                weekAgo.setDate(weekAgo.getDate() - 7);

                const monthAgo = new Date(today);
                monthAgo.setDate(monthAgo.getDate() - 30);

                result = result.filter(payment => {
                    const paymentDate = new Date(payment.payment_date);

                    if (this.dateFilter === 'today') {
                        return paymentDate >= today;
                    } else if (this.dateFilter === 'yesterday') {
                        return paymentDate >= yesterday && paymentDate < today;
                    } else if (this.dateFilter === 'week') {
                        return paymentDate >= weekAgo;
                    } else if (this.dateFilter === 'month') {
                        return paymentDate >= monthAgo;
                    }

                    return true;
                });
            }

            // Apply pagination
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            return result.slice(startIndex, startIndex + this.itemsPerPage);
        },

        totalPages() {
            let filteredCount = this.payments.length;

            if (this.searchQuery || this.statusFilter || this.paymentMethodFilter || this.dateFilter) {
                filteredCount = this.payments.filter(payment => {
                    let matches = true;

                    if (this.searchQuery) {
                        const query = this.searchQuery.toLowerCase();
                        matches = payment.reference_id.toLowerCase().includes(query) ||
                            payment.order_number.toLowerCase().includes(query) ||
                            payment.customer_name.toLowerCase().includes(query);
                    }

                    if (matches && this.statusFilter) {
                        matches = payment.status === this.statusFilter;
                    }

                    if (matches && this.paymentMethodFilter) {
                        matches = payment.payment_method === this.paymentMethodFilter;
                    }

                    if (matches && this.dateFilter) {
                        const today = new Date();
                        today.setHours(0, 0, 0, 0);

                        const yesterday = new Date(today);
                        yesterday.setDate(yesterday.getDate() - 1);

                        const weekAgo = new Date(today);
                        weekAgo.setDate(weekAgo.getDate() - 7);

                        const monthAgo = new Date(today);
                        monthAgo.setDate(monthAgo.getDate() - 30);

                        const paymentDate = new Date(payment.payment_date);

                        if (this.dateFilter === 'today') {
                            matches = paymentDate >= today;
                        } else if (this.dateFilter === 'yesterday') {
                            matches = paymentDate >= yesterday && paymentDate < today;
                        } else if (this.dateFilter === 'week') {
                            matches = paymentDate >= weekAgo;
                        } else if (this.dateFilter === 'month') {
                            matches = paymentDate >= monthAgo;
                        }
                    }

                    return matches;
                }).length;
            }

            return Math.max(1, Math.ceil(filteredCount / this.itemsPerPage));
        },

        isBankTransfer() {
            return this.selectedPayment.payment_method === 'bank_transfer';
        },

        isPromptpay() {
            return this.selectedPayment.payment_method === 'promptpay';
        },

        isCreditCard() {
            return this.selectedPayment.payment_method === 'credit_card';
        }
    },
    mounted() {
        this.fetchPayments();
    },
    methods: {
        async fetchPayments() {
            await this.fetchAllPayments();
        },

        formatDate(dateString) {
            if (!dateString) return '-';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('th-TH', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            }).format(date);
        },

        formatDateTime(dateString) {
            if (!dateString) return '-';
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('th-TH', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric'
            }).format(date);
        },

        formatNumber(number) {
            return new Intl.NumberFormat('th-TH').format(number);
        },

        getPaymentMethodName(method) {
            switch (method) {
                case 'bank_transfer':
                    return 'โอนผ่านธนาคาร';
                case 'credit_card':
                    return 'บัตรเครดิต';
                case 'promptpay':
                    return 'พร้อมเพย์';
                default:
                    return '-';
            }
        },

        getStatusName(status) {
            switch (status) {
                case 'pending':
                    return 'รอตรวจสอบ';
                case 'approved':
                    return 'อนุมัติแล้ว';
                case 'rejected':
                    return 'ปฏิเสธ';
                default:
                    return '-';
            }
        },

        viewPayment(payment) {
            this.selectedPayment = payment;
            this.showDetailsModal = true;
        },

        confirmApprovePayment(payment) {
            this.paymentToApprove = payment;
            this.showApproveModal = true;
        },

        async approvePayment() {
            try {
                await this.updatePaymentStatus(this.paymentToApprove.id, {
                    status: 'approved',
                    verified_by: 'Admin User',
                    verified_note: this.approveNote
                });

                // Refresh payment data
                await this.fetchPayments();

                // Close modals
                this.showApproveModal = false;
                this.showDetailsModal = false;
            } catch (err) {
                console.error('Error approving payment:', err);
                alert('เกิดข้อผิดพลาดในการอนุมัติการชำระเงิน กรุณาลองใหม่อีกครั้ง');
            }
        },

        confirmRejectPayment(payment) {
            this.paymentToReject = payment;
            this.showRejectModal = true;
        },

        async rejectPayment() {
            if (!this.rejectReason) {
                this.rejectReasonError = 'กรุณาระบุเหตุผลในการปฏิเสธ';
                return;
            }

            try {
                await this.updatePaymentStatus(this.paymentToReject.id, {
                    status: 'rejected',
                    verified_by: 'Admin User',
                    verified_note: this.rejectReason
                });

                // Refresh payment data
                await this.fetchPayments();

                // Close modals
                this.showRejectModal = false;
                this.showDetailsModal = false;
            } catch (err) {
                console.error('Error rejecting payment:', err);
                alert('เกิดข้อผิดพลาดในการปฏิเสธการชำระเงิน กรุณาลองใหม่อีกครั้ง');
            }
        },

        changePage(page) {
            this.currentPage = page;
        },

        openImagePreview(imageUrl) {
            this.previewImageUrl = imageUrl;
            this.showImagePreview = true;
        },

        printPaymentDetails() {
            window.print();
        },

        maskCardNumber(cardNumber) {
            if (!cardNumber) return '-';
            return cardNumber.replace(/\d{12}(\d{4})/, '**** **** **** $1');
        }
    }
};
</script>

<style scoped>
.payments-management
{
    padding: 20px;
}

.payments-management .page-header
{
    margin-bottom: 20px;
}

.stats-cards
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.stat-card
{
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    flex: 1;
    margin-right: 20px;
    display: flex;
    align-items: center;
}

.stat-card:last-child
{
    margin-right: 0;
}

.stat-icon
{
    font-size: 24px;
    margin-right: 10px;
}

.stat-icon.pending
{
    color: #f39c12;
}

.stat-icon.approved
{
    color: #27ae60;
}

.stat-icon.rejected
{
    color: #e74c3c;
}

.stat-icon.total
{
    color: #3498db;
}

.stat-content
{
    flex: 1;
}

.stat-value
{
    font-size: 24px;
    font-weight: bold;
}

.filter-section
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.search-box
{
    flex: 1;
    margin-right: 20px;
}

.search-box input
{
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.filter-box
{
    display: flex;
    align-items: center;
}

.filter-box select
{
    margin-right: 10px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.loading-container,
.error-container,
.empty-state
{
    text-align: center;
    padding: 20px;
}

.loading-spinner
{
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 10px;
}

@keyframes spin
{
    0%
    {
        transform: rotate(0deg);
    }

    100%
    {
        transform: rotate(360deg);
    }
}

.retry-button
{
    background-color: #3498db;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.retry-button:hover
{
    background-color: #2980b9;
}

.table-container
{
    overflow-x: auto;
}

.data-table
{
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td
{
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
}

.data-table th
{
    background-color: #f9f9f9;
}

.status-badge
{
    padding: 5px 10px;
    border-radius: 8px;
    color: #fff;
    font-weight: bold;
}

.status-badge.pending
{
    background-color: #f39c12;
}

.status-badge.approved
{
    background-color: #27ae60;
}

.status-badge.rejected
{
    background-color: #e74c3c;
}

.actions
{
    display: flex;
    align-items: center;
}

.actions button
{
    margin-right: 10px;
    padding: 5px 10px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.actions button:last-child
{
    margin-right: 0;
}

.view-btn
{
    background-color: #3498db;
    color: #fff;
}

.view-btn:hover
{
    background-color: #2980b9;
}

.approve-btn
{
    background-color: #27ae60;
    color: #fff;
}

.approve-btn:hover
{
    background-color: #229954;
}

.reject-btn
{
    background-color: #e74c3c;
    color: #fff;
}

.reject-btn:hover
{
    background-color: #c0392b;
}

.pagination
{
    text-align: center;
    margin-top: 20px;
}

.pagination button
{
    padding: 5px 10px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    margin: 0 5px;
}

.pagination button:disabled
{
    background-color: #ddd;
    cursor: not-allowed;
}

.pagination span
{
    font-weight: bold;
}

.modal-overlay
{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content
{
    background-color: #fff;
    border-radius: 8px;
    padding: 20px;
    width: 90%;
    max-width: 600px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.modal-header h2
{
    margin: 0;
}

.close-button
{
    background-color: transparent;
    border: none;
    font-size: 24px;
    cursor: pointer;
}

.modal-body
{
    margin-bottom: 20px;
}

.payment-summary
{
    margin-bottom: 20px;
}

.payment-summary .summary-item
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.summary-item .label
{
    font-weight: bold;
}

.summary-item .amount
{
    color: #27ae60;
    font-weight: bold;
}

.form-group
{
    margin-bottom: 20px;
}

.form-group label
{
    display: block;
    margin-bottom: 5px;
}

.form-group textarea
{
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.error-message
{
    color: #e74c3c;
    font-size: 14px;
    margin-top: 5px;
}

.modal-footer
{
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
}

.modal-footer button
{
    margin-left: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.cancel-button
{
    background-color: #ddd;
}

.cancel-button:hover
{
    background-color: #ccc;
}

.approve-button
{
    background-color: #27ae60;
    color: #fff;
}

.approve-button:hover
{
    background-color: #229954;
}

.reject-button
{
    background-color: #e74c3c;
    color: #fff;
}

.reject-button:hover
{
    background-color: #c0392b;
}

.print-button
{
    background-color: #3498db;
    color: #fff;
}

.print-button:hover
{
    background-color: #2980b9;
}

.payment-details-modal
{
    max-width: 800px;
}

.payment-details
{
    margin-bottom: 20px;
}

.payment-info-section
{
    margin-bottom: 20px;
}

.payment-info-section h3
{
    margin-bottom: 10px;
}

.info-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.info-item
{
    display: flex;
    justify-content: space-between;
}

.info-item .label
{
    font-weight: bold;
}

.info-item .amount
{
    color: #27ae60;
    font-weight: bold;
}

.payment-evidence
{
    text-align: center;
}

.payment-evidence img
{
    max-width: 100%;
    cursor: pointer;
}

.no-evidence
{
    color: #999;
}

.image-preview-container
{
    position: relative;
    max-width: 90%;
    max-height: 90%;
}

.image-preview-container img
{
    max-width: 100%;
    max-height: 100%;
}

.image-preview-container .close-button
{
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: rgba(0, 0, 0, 0.5);
    color: #fff;
    border: none;
    font-size: 24px;
    cursor: pointer;
}
</style>