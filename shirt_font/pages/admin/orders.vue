<template>
	<AdminLayout>
		<div class="orders-management">
			<div class="page-header">
				<h1>จัดการออเดอร์</h1>
			</div>

			<div class="stats-cards">
				<div class="stat-card">
					<div class="stat-icon pending">
						<i class="fas fa-clock"></i>
					</div>
					<div class="stat-content">
						<div class="stat-title">รอดำเนินการ</div>
						<div class="stat-value">{{ pendingOrdersCount }}</div>
					</div>
				</div>
				<div class="stat-card">
					<div class="stat-icon processing">
						<i class="fas fa-box-open"></i>
					</div>
					<div class="stat-content">
						<div class="stat-title">กำลังจัดส่ง</div>
						<div class="stat-value">{{ processingOrdersCount }}</div>
					</div>
				</div>
				<div class="stat-card">
					<div class="stat-icon delivered">
						<i class="fas fa-check-circle"></i>
					</div>
					<div class="stat-content">
						<div class="stat-title">จัดส่งสำเร็จ</div>
						<div class="stat-value">{{ deliveredOrdersCount }}</div>
					</div>
				</div>
				<div class="stat-card">
					<div class="stat-icon cancelled">
						<i class="fas fa-times-circle"></i>
					</div>
					<div class="stat-content">
						<div class="stat-title">ยกเลิก</div>
						<div class="stat-value">{{ cancelledOrdersCount }}</div>
					</div>
				</div>
			</div>

			<div class="filter-section">
				<div class="search-box">
					<input type="text" v-model="searchQuery" placeholder="ค้นหาออเดอร์..." />
				</div>
				<div class="filter-box">
					<select v-model="statusFilter">
						<option value="">ทุกสถานะ</option>
						<option value="pending">รอดำเนินการ</option>
						<option value="processing">กำลังจัดส่ง</option>
						<option value="delivered">จัดส่งสำเร็จ</option>
						<option value="cancelled">ยกเลิก</option>
					</select>
					<select v-model="paymentFilter">
						<option value="">ทุกการชำระเงิน</option>
						<option value="paid">ชำระเงินแล้ว</option>
						<option value="unpaid">ยังไม่ชำระเงิน</option>
					</select>
					<select v-model="dateFilter">
						<option value="">ทุกวัน</option>
						<option value="today">วันนี้</option>
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
				<button @click="fetchOrders" class="retry-button">ลองใหม่</button>
			</div>

			<div v-else class="orders-container">
				<table class="orders-table">
					<thead>
						<tr>
							<th>รหัสออเดอร์</th>
							<th>ลูกค้า</th>
							<th>วันที่สั่งซื้อ</th>
							<th>ยอดรวม</th>
							<th>การชำระเงิน</th>
							<th>สถานะ</th>
							<th>การจัดการ</th>
						</tr>
					</thead>
					<tbody>
						<tr v-for="order in paginatedOrders" :key="order.id" @click="viewOrderDetails(order)" class="order-row">
							<td class="order-id">{{ order.orderNumber }}</td>
							<td>{{ order.customer.name }}</td>
							<td>{{ formatDate(order.orderDate) }}</td>
							<td class="order-total">฿{{ formatPrice(order.total) }}</td>
							<td>
								<span class="payment-badge" :class="order.paymentStatus">
									{{ getPaymentStatusText(order.paymentStatus) }}
								</span>
							</td>
							<td>
								<span class="status-badge" :class="order.status">
									{{ getOrderStatusText(order.status) }}
								</span>
							</td>
							<td class="actions">
								<div class="dropdown">
									<button class="dropdown-toggle">
										<i class="fas fa-ellipsis-v"></i>
									</button>
									<div class="dropdown-menu">
										<button @click.stop="viewOrderDetails(order)">
											<i class="fas fa-eye"></i> ดูรายละเอียด
										</button>
										<button @click.stop="updateOrderStatus(order, 'processing')" v-if="order.status === 'pending'">
											<i class="fas fa-box"></i> เริ่มจัดส่ง
										</button>
										<button @click.stop="updateOrderStatus(order, 'delivered')" v-if="order.status === 'processing'">
											<i class="fas fa-check"></i> ยืนยันการจัดส่ง
										</button>
										<button @click.stop="confirmCancelOrder(order)"
											v-if="order.status !== 'delivered' && order.status !== 'cancelled'">
											<i class="fas fa-times"></i> ยกเลิกออเดอร์
										</button>
										<button @click.stop="printOrder(order)">
											<i class="fas fa-print"></i> พิมพ์ใบเสร็จ
										</button>
									</div>
								</div>
							</td>
						</tr>
					</tbody>
				</table>

				<div v-if="paginatedOrders.length === 0" class="empty-state">
					<i class="fas fa-shopping-cart fa-3x"></i>
					<p>ไม่พบรายการสั่งซื้อที่ตรงกับเงื่อนไขการค้นหา</p>
				</div>

				<div class="pagination" v-if="totalPages > 1">
					<button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
						&laquo; ก่อนหน้า
					</button>
					<span>หน้า {{ currentPage }} จาก {{ totalPages }}</span>
					<button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
						ถัดไป &raquo;
					</button>
				</div>
			</div>
		</div>

		<!-- Order Details Modal -->
		<div v-if="showDetailsModal" class="modal-overlay">
			<div class="modal-content large-modal">
				<div class="modal-header">
					<h2>รายละเอียดออเดอร์ #{{ selectedOrder.orderNumber }}</h2>
					<button class="close-button" @click="closeDetailsModal">&times;</button>
				</div>
				<div class="modal-body">
					<div class="order-status-timeline">
						<div class="timeline-step"
							:class="{ active: selectedOrder.status === 'pending' || selectedOrder.status === 'processing' || selectedOrder.status === 'delivered' }">
							<div class="step-icon"><i class="fas fa-shopping-cart"></i></div>
							<div class="step-label">รับออเดอร์แล้ว</div>
						</div>
						<div class="timeline-line"></div>
						<div class="timeline-step"
							:class="{ active: selectedOrder.status === 'processing' || selectedOrder.status === 'delivered' }">
							<div class="step-icon"><i class="fas fa-box"></i></div>
							<div class="step-label">กำลังจัดส่ง</div>
						</div>
						<div class="timeline-line"></div>
						<div class="timeline-step" :class="{ active: selectedOrder.status === 'delivered' }">
							<div class="step-icon"><i class="fas fa-check-circle"></i></div>
							<div class="step-label">จัดส่งสำเร็จ</div>
						</div>
					</div>

					<div class="order-details-grid">
						<div class="order-info-panel">
							<h3>ข้อมูลออเดอร์</h3>
							<div class="info-row">
								<div class="label">รหัสออเดอร์:</div>
								<div>{{ selectedOrder.orderNumber }}</div>
							</div>
							<div class="info-row">
								<div class="label">วันที่สั่งซื้อ:</div>
								<div>{{ formatDate(selectedOrder.orderDate) }}</div>
							</div>
							<div class="info-row">
								<div class="label">สถานะ:</div>
								<div>
									<span class="status-badge" :class="selectedOrder.status">
										{{ getOrderStatusText(selectedOrder.status) }}
									</span>
								</div>
							</div>
							<div class="info-row">
								<div class="label">การชำระเงิน:</div>
								<div>
									<span class="payment-badge" :class="selectedOrder.paymentStatus">
										{{ getPaymentStatusText(selectedOrder.paymentStatus) }}
									</span>
								</div>
							</div>
							<div class="info-row" v-if="selectedOrder.paymentMethod">
								<div class="label">ช่องทางการชำระเงิน:</div>
								<div>{{ selectedOrder.paymentMethod }}</div>
							</div>
						</div>

						<div class="customer-info-panel">
							<h3>ข้อมูลลูกค้า</h3>
							<div class="info-row">
								<div class="label">ชื่อลูกค้า:</div>
								<div>{{ selectedOrder.customer?.name }}</div>
							</div>
							<div class="info-row">
								<div class="label">อีเมล:</div>
								<div>{{ selectedOrder.customer?.email }}</div>
							</div>
							<div class="info-row">
								<div class="label">เบอร์โทร:</div>
								<div>{{ selectedOrder.customer?.phone || '-' }}</div>
							</div>
						</div>

						<div class="shipping-info-panel">
							<h3>ที่อยู่จัดส่ง</h3>
							<div class="address-box" v-if="selectedOrder.shipping">
								<p>{{ selectedOrder.shipping.name }}</p>
								<p>{{ selectedOrder.shipping.address }}</p>
								<p>{{ selectedOrder.shipping.phone }}</p>
							</div>
							<div v-if="selectedOrder.trackingNumber" class="tracking-info">
								<div class="label">หมายเลขพัสดุ:</div>
								<div>{{ selectedOrder.trackingNumber }}</div>
							</div>
							<div v-if="selectedOrder.shippingMethod" class="tracking-info">
								<div class="label">วิธีการจัดส่ง:</div>
								<div>{{ selectedOrder.shippingMethod }}</div>
							</div>
						</div>
					</div>

					<div class="order-items-section">
						<h3>รายการสินค้า</h3>
						<div class="order-items-table">
							<table>
								<thead>
									<tr>
										<th width="60px">รูปภาพ</th>
										<th>สินค้า</th>
										<th>ตัวเลือก</th>
										<th width="80px">จำนวน</th>
										<th width="120px">ราคา/หน่วย</th>
										<th width="120px">ราคารวม</th>
									</tr>
								</thead>
								<tbody>
									<tr v-for="(item, index) in selectedOrder.items" :key="index">
										<td>
											<img :src="item.image || 'https://via.placeholder.com/50'" :alt="item.name"
												class="product-thumbnail">
										</td>
										<td>{{ item.name }}</td>
										<td>
											<div v-if="item.variants && item.variants.length > 0" class="variants-list">
												<span v-for="(variant, idx) in item.variants" :key="idx" class="variant-tag">
													{{ variant.type }}: {{ variant.value }}
												</span>
											</div>
											<span v-else>-</span>
										</td>
										<td>{{ item.quantity }}</td>
										<td>฿{{ formatPrice(item.price) }}</td>
										<td>฿{{ formatPrice(item.price * item.quantity) }}</td>
									</tr>
								</tbody>
								<tfoot>
									<tr>
										<td colspan="5" class="text-right">ยอดรวมค่าสินค้า:</td>
										<td>฿{{ formatPrice(selectedOrder.subtotal || 0) }}</td>
									</tr>
									<tr>
										<td colspan="5" class="text-right">ค่าจัดส่ง:</td>
										<td>฿{{ formatPrice(selectedOrder.shippingFee || 0) }}</td>
									</tr>
									<tr v-if="selectedOrder.discount">
										<td colspan="5" class="text-right">ส่วนลด:</td>
										<td>-฿{{ formatPrice(selectedOrder.discount || 0) }}</td>
									</tr>
									<tr class="total-row">
										<td colspan="5" class="text-right">ยอดชำระทั้งหมด:</td>
										<td>฿{{ formatPrice(selectedOrder.total || 0) }}</td>
									</tr>
								</tfoot>
							</table>
						</div>
					</div>

					<div class="order-history-section">
						<h3>ประวัติการสั่งซื้อ</h3>
						<div class="history-timeline">
							<div v-for="(history, index) in selectedOrder.statusHistory" :key="index" class="history-item">
								<div class="history-dot"></div>
								<div class="history-content">
									<div class="history-status">
										<span class="status-badge" :class="history.status">
											{{ getOrderStatusText(history.status) }}
										</span>
									</div>
									<div class="history-date">{{ formatDateTime(history.timestamp) }}</div>
									<div class="history-note" v-if="history.note">{{ history.note }}</div>
								</div>
							</div>
						</div>
					</div>

					<div class="order-note-section" v-if="selectedOrder.note">
						<h3>หมายเหตุจากลูกค้า</h3>
						<div class="note-content">
							<p>{{ selectedOrder.note }}</p>
						</div>
					</div>
				</div>
				<div class="modal-footer">
					<button class="cancel-button" @click="closeDetailsModal">ปิด</button>
					<button class="action-button warning" @click="confirmCancelOrder(selectedOrder)"
						v-if="selectedOrder.status !== 'delivered' && selectedOrder.status !== 'cancelled'">
						ยกเลิกคำสั่งซื้อ
					</button>
					<button class="action-button" @click="openUpdateStatusModal"
						v-if="selectedOrder.status !== 'delivered' && selectedOrder.status !== 'cancelled'">
						อัพเดทสถานะ
					</button>
					<button class="action-button" @click="printOrder(selectedOrder)">
						<i class="fas fa-print"></i> พิมพ์ใบเสร็จ
					</button>
				</div>
			</div>
		</div>

		<!-- Update Status Modal -->
		<div v-if="showStatusModal" class="modal-overlay">
			<div class="modal-content">
				<div class="modal-header">
					<h2>อัพเดทสถานะคำสั่งซื้อ</h2>
					<button class="close-button" @click="closeStatusModal">&times;</button>
				</div>
				<div class="modal-body">
					<div class="form-group">
						<label for="orderStatus">เลือกสถานะใหม่</label>
						<select id="orderStatus" v-model="newStatus">
							<option value="pending">รอดำเนินการ</option>
							<option value="processing">กำลังจัดส่ง</option>
							<option value="delivered">จัดส่งสำเร็จ</option>
						</select>
					</div>
					<div class="form-group" v-if="newStatus === 'processing'">
						<label for="trackingNumber">เลขพัสดุ</label>
						<input type="text" id="trackingNumber" v-model="trackingNumber" placeholder="เช่น TH123456789">
					</div>
					<div class="form-group">
						<label for="statusNote">หมายเหตุ (ถ้ามี)</label>
						<textarea id="statusNote" v-model="statusNote" rows="3"
							placeholder="เพิ่มหมายเหตุเกี่ยวกับการอัพเดทสถานะนี้"></textarea>
					</div>
				</div>
				<div class="modal-footer">
					<button class="cancel-button" @click="closeStatusModal">ยกเลิก</button>
					<button class="save-button" @click="saveOrderStatus">บันทึก</button>
				</div>
			</div>
		</div>

		<!-- Cancel Order Confirmation Modal -->
		<div v-if="showCancelModal" class="modal-overlay">
			<div class="modal-content delete-modal">
				<div class="modal-header">
					<h2>ยืนยันการยกเลิกคำสั่งซื้อ</h2>
					<button class="close-button" @click="closeCancelModal">&times;</button>
				</div>
				<div class="modal-body">
					<p>คุณต้องการยกเลิกคำสั่งซื้อ #{{ orderToCancel?.orderNumber }} ใช่หรือไม่?</p>
					<div class="form-group">
						<label for="cancelReason">เหตุผลในการยกเลิก</label>
						<textarea id="cancelReason" v-model="cancelReason" rows="3" required></textarea>
					</div>
					<p class="warning">การยกเลิกคำสั่งซื้อจะไม่สามารถเปลี่ยนกลับได้</p>
				</div>
				<div class="modal-footer">
					<button class="regular-button" @click="closeCancelModal">ไม่ยกเลิก</button>
					<button class="delete-button" @click="cancelOrder">ยืนยันการยกเลิก</button>
				</div>
			</div>
		</div>
	</AdminLayout>
</template>

<script>
import AdminLayout from '~/components/admin/AdminLayout.vue';
import useOrder from '~/composables/useOrder';
import usePayment from '~/composables/usePayment';

export default {
	components: {
		AdminLayout
	},
	setup() {
		const {
			orders,
			loading,
			error,
			orderStats,
			fetchAllOrders,
			getOrderById,
			updateOrderStatus: updateOrderStatusApi,
			cancelOrder: cancelOrderApi
		} = useOrder();

		const {
			getOrderPayments,
			updatePaymentStatus
		} = usePayment();

		return {
			orders,
			loading,
			error,
			orderStats,
			fetchAllOrders,
			getOrderById,
			updateOrderStatusApi,
			cancelOrderApi,
			getOrderPayments,
			updatePaymentStatus
		};
	},
	data() {
		return {
			searchQuery: '',
			statusFilter: '',
			paymentFilter: '',
			dateFilter: '',
			currentPage: 1,
			itemsPerPage: 10,
			showDetailsModal: false,
			showStatusModal: false,
			showCancelModal: false,
			selectedOrder: {},
			orderToCancel: null,
			newStatus: '',
			trackingNumber: '',
			statusNote: '',
			cancelReason: ''
		};
	},
	computed: {
		filteredOrders() {
			let result = this.orders;

			// Apply search filter
			if (this.searchQuery) {
				const query = this.searchQuery.toLowerCase();
				result = result.filter(order =>
					order.orderNumber.toLowerCase().includes(query) ||
					order.customer.name.toLowerCase().includes(query)
				);
			}

			// Apply status filter
			if (this.statusFilter) {
				result = result.filter(order => order.status === this.statusFilter);
			}

			// Apply payment filter
			if (this.paymentFilter) {
				result = result.filter(order => {
					if (this.paymentFilter === 'paid') {
						return order.paymentStatus === 'paid';
					} else if (this.paymentFilter === 'unpaid') {
						return order.paymentStatus === 'unpaid';
					}
					return true;
				});
			}

			// Apply date filter
			if (this.dateFilter) {
				const today = new Date();
				today.setHours(0, 0, 0, 0);

				const weekAgo = new Date(today);
				weekAgo.setDate(weekAgo.getDate() - 7);

				const monthAgo = new Date(today);
				monthAgo.setDate(monthAgo.getDate() - 30);

				result = result.filter(order => {
					const orderDate = new Date(order.orderDate);

					if (this.dateFilter === 'today') {
						return orderDate >= today;
					} else if (this.dateFilter === 'week') {
						return orderDate >= weekAgo;
					} else if (this.dateFilter === 'month') {
						return orderDate >= monthAgo;
					}

					return true;
				});
			}

			return result;
		},
		paginatedOrders() {
			const startIndex = (this.currentPage - 1) * this.itemsPerPage;
			return this.filteredOrders.slice(startIndex, startIndex + this.itemsPerPage);
		},
		totalPages() {
			return Math.max(1, Math.ceil(this.filteredOrders.length / this.itemsPerPage));
		},
		pendingOrdersCount() {
			return this.orders.filter(order => order.status === 'pending').length;
		},
		processingOrdersCount() {
			return this.orders.filter(order => order.status === 'processing').length;
		},
		deliveredOrdersCount() {
			return this.orders.filter(order => order.status === 'delivered').length;
		},
		cancelledOrdersCount() {
			return this.orders.filter(order => order.status === 'cancelled').length;
		}
	},
	mounted() {
		this.fetchOrders();
	},
	methods: {
		async fetchOrders() {
			await this.fetchAllOrders();
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
				hour: '2-digit',
				minute: '2-digit'
			}).format(date);
		},

		formatPrice(price) {
			if (!price) return '0';
			return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
		},

		formatAddress(address) {
			if (!address) return '-';

			return `${address.name} (${address.phone})
${address.address}
แขวง/ตำบล ${address.subdistrict || '-'} เขต/อำเภอ ${address.district || '-'}
จังหวัด ${address.province || '-'} ${address.postal_code || '-'}`;
		},

		getOrderStatusText(status) {
			switch (status) {
				case 'pending': return 'รอดำเนินการ';
				case 'processing': return 'กำลังจัดส่ง';
				case 'delivered': return 'จัดส่งสำเร็จ';
				case 'cancelled': return 'ยกเลิก';
				default: return status;
			}
		},

		getPaymentStatusText(status) {
			switch (status) {
				case 'paid': return 'ชำระเงินแล้ว';
				case 'unpaid': return 'ยังไม่ชำระเงิน';
				default: return status;
			}
		},

		changePage(page) {
			if (page > 0 && page <= this.totalPages) {
				this.currentPage = page;
			}
		},

		viewOrderDetails(order) {
			this.selectedOrder = order;
			this.showDetailsModal = true;
		},

		openUpdateStatusModal() {
			this.newStatus = this.selectedOrder.status;
			this.trackingNumber = this.selectedOrder.trackingNumber || '';
			this.statusNote = '';
			this.showStatusModal = true;
		},

		async saveOrderStatus() {
			try {
				await this.updateOrderStatusApi(this.selectedOrder.id, {
					status: this.newStatus,
					tracking_number: this.trackingNumber,
					note: this.statusNote
				});

				// If we're updating to processing status and this requires payment verification
				if (this.newStatus === 'processing' && this.selectedOrder.paymentStatus === 'pending') {
					// Get related payment
					const paymentResponse = await this.getOrderPayments(this.selectedOrder.id);
					if (paymentResponse && paymentResponse.length > 0) {
						// Update the payment status to approved
						const payment = paymentResponse[0];
						await this.updatePaymentStatus(payment.id, {
							status: 'approved',
							verified_by: 'Admin User',
							verified_note: 'Auto-approved when order status changed to processing'
						});
					}
				}

				// Refresh orders
				await this.fetchOrders();

				// If we're looking at order details, update the selected order
				if (this.showDetailsModal) {
					const updatedOrder = await this.getOrderById(this.selectedOrder.id);
					this.selectedOrder = updatedOrder;
				}

				this.closeStatusModal();
			} catch (err) {
				console.error('Error updating order status:', err);
				alert('ไม่สามารถอัพเดทสถานะคำสั่งซื้อได้ กรุณาลองใหม่อีกครั้ง');
			}
		},

		async cancelOrder() {
			try {
				await this.cancelOrderApi(this.orderToCancel.id, this.cancelReason);

				// If the order had a pending payment, we should also cancel/reject it
				const paymentResponse = await this.getOrderPayments(this.orderToCancel.id);
				if (paymentResponse && paymentResponse.length > 0) {
					const payment = paymentResponse[0];
					if (payment.status === 'pending') {
						await this.updatePaymentStatus(payment.id, {
							status: 'rejected',
							verified_by: 'Admin User',
							verified_note: `Order cancelled: ${this.cancelReason}`
						});
					}
				}

				// Refresh orders
				await this.fetchOrders();

				// If we're looking at order details, close the modal
				this.closeCancelModal();
				if (this.selectedOrder.id === this.orderToCancel.id) {
					this.closeDetailsModal();
				}
			} catch (err) {
				console.error('Error cancelling order:', err);
				alert('ไม่สามารถยกเลิกคำสั่งซื้อได้ กรุณาลองใหม่อีกครั้ง');
			}
		},

		confirmCancelOrder(order) {
			this.orderToCancel = order;
			this.cancelReason = '';
			this.showCancelModal = true;
		},

		closeDetailsModal() {
			this.showDetailsModal = false;
		},

		closeStatusModal() {
			this.showStatusModal = false;
		},

		closeCancelModal() {
			this.showCancelModal = false;
		},

		printOrder(order) {
			// In a real app, you would generate a printable version of the order
			console.log('Printing order:', order);
		}
	}
};
</script>

<style scoped>
.orders-management
{
	padding: 20px;
}

.page-header
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
	flex: 1;
	display: flex;
	align-items: center;
	padding: 10px;
	border-radius: 8px;
	background-color: #f5f5f5;
	margin-right: 10px;
}

.stat-card:last-child
{
	margin-right: 0;
}

.stat-icon
{
	width: 40px;
	height: 40px;
	border-radius: 50%;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 24px;
	margin-right: 10px;
}

.stat-content
{
	flex: 1;
}

.stat-title
{
	font-size: 14px;
	color: #888;
}

.stat-value
{
	font-size: 18px;
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
	margin-right: 10px;
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
	flex: 2;
	justify-content: space-between;
}

.filter-box select
{
	flex: 1;
	padding: 10px;
	border: 1px solid #ddd;
	border-radius: 8px;
	margin-right: 10px;
}

.filter-box select:last-child
{
	margin-right: 0;
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
	width: 40px;
	height: 40px;
	border: 4px solid #ddd;
	border-top: 4px solid #333;
	border-radius: 50%;
	margin: 0 auto 10px;
	animation: spin 1s linear infinite;
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

.orders-container
{
	overflow-x: auto;
}

.orders-table
{
	width: 100%;
	border-collapse: collapse;
	border-radius: 8px;
	margin-bottom: 20px;
}

.orders-table th,
.orders-table td
{
	padding: 10px;
	border: 1px solid #ddd;
	text-align: left;
}

.orders-table th
{
	background-color: #f5f5f5;
}

.order-row
{
	cursor: pointer;
}

.order-row:hover
{
	background-color: #f9f9f9;
}

.order-id
{
	font-weight: bold;
}

.order-total
{
	font-weight: bold;
	color: #333;
}

.payment-badge,
.status-badge
{
	display: inline-block;
	padding: 5px 10px;
	border-radius: 8px;
	text-align: center;
	font-size: 12px;
	color: #fff;
}

.payment-badge.paid
{
	background-color: #4caf50;
}

.payment-badge.unpaid
{
	background-color: #f44336;
}

.status-badge.pending
{
	background-color: #ff9800;
}

.status-badge.processing
{
	background-color: #2196f3;
}

.status-badge.delivered
{
	background-color: #4caf50;
}

.status-badge.cancelled
{
	background-color: #f44336;
}

.actions
{
	position: relative;
}

.dropdown
{
	position: relative;
}

.dropdown-toggle
{
	background: none;
	border: none;
	cursor: pointer;
	font-size: 16px;
}

.dropdown-menu
{
	position: absolute;
	top: 100%;
	right: 0;
	background-color: #fff;
	border: 1px solid #ddd;
	border-radius: 8px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	display: none;
	z-index: 1;
}

.dropdown-menu button
{
	display: block;
	width: 100%;
	padding: 10px;
	background: none;
	border: none;
	text-align: left;
	cursor: pointer;
}

.dropdown-menu button:hover
{
	background-color: #f5f5f5;
}

.dropdown:hover .dropdown-menu
{
	display: block;
}

.pagination
{
	display: flex;
	justify-content: center;
	align-items: center;
}

.pagination button
{
	padding: 10px 20px;
	border: 1px solid #ddd;
	background-color: #fff;
	cursor: pointer;
	margin: 0 5px;
	border-radius: 8px;
}

.pagination button:disabled
{
	cursor: not-allowed;
	opacity: 0.5;
}

.pagination span
{
	font-size: 14px;
	color: #888;
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
	justify-content: center;
	align-items: center;
	z-index: 1000;
}

.modal-content
{
	background-color: #fff;
	border-radius: 8px;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	width: 90%;
	max-width: 600px;
	max-height: 90%;
	overflow-y: auto;
}

.large-modal
{
	max-width: 800px;
}

.modal-header
{
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 20px;
	border-bottom: 1px solid #ddd;
}

.modal-header h2
{
	margin: 0;
	font-size: 18px;
}

.close-button
{
	background: none;
	border: none;
	font-size: 24px;
	cursor: pointer;
}

.modal-body
{
	padding: 20px;
}

.modal-footer
{
	display: flex;
	justify-content: flex-end;
	padding: 20px;
	border-top: 1px solid #ddd;
}

.modal-footer button
{
	padding: 10px 20px;
	border: none;
	border-radius: 8px;
	cursor: pointer;
	margin-left: 10px;
}

.cancel-button
{
	background-color: #f44336;
	color: #fff;
}

.save-button
{
	background-color: #4caf50;
	color: #fff;
}

.regular-button
{
	background-color: #ddd;
	color: #333;
}

.delete-button
{
	background-color: #f44336;
	color: #fff;
}

.action-button
{
	background-color: #2196f3;
	color: #fff;
}

.action-button.warning
{
	background-color: #ff9800;
}

.print-button
{
	background-color: #4caf50;
	color: #fff;
	text-decoration: none;
	z-index: 1;
	padding: 10px 20px;
	border-radius: 8px;
	display: inline-block;
	cursor: pointer;
}

.order-status-timeline
{
	display: flex;
	align-items: center;
	margin-bottom: 20px;
}

.timeline-step
{
	display: flex;
	flex-direction: column;
	align-items: center;
	position: relative;
}

.timeline-step .step-icon
{
	font-size: 24px;
	margin-bottom: 5px;
}

.timeline-step .step-label
{
	font-size: 12px;
	color: #888;
}

.timeline-step.active .step-icon
{
	color: #4caf50;
}

.timeline-line
{
	flex: 1;
	height: 2px;
	background-color: #ddd;
	margin: 0 10px;
}

.order-details-grid
{
	display: grid;
	grid-template-columns: 1fr 1fr 1fr;
	gap: 20px;
	margin-bottom: 20px;
}

.order-info-panel,
.customer-info-panel,
.shipping-info-panel
{
	background-color: #f5f5f5;
	padding: 20px;
	border-radius: 8px;
}

.order-info-panel h3,
.customer-info-panel h3,
.shipping-info-panel h3
{
	margin-top: 0;
	font-size: 16px;
}

.info-row
{
	display: flex;
	justify-content: space-between;
	margin-bottom: 10px;
}

.info-row .label
{
	font-weight: bold;
	color: #888;
}

.address-box
{
	background-color: #fff;
	padding: 10px;
	border-radius: 8px;
	border: 1px solid #ddd;
	margin-top: 10px;
}

.order-items-section,
.order-history-section,
.order-note-section
{
	margin-bottom: 20px;
}

.order-items-table
{
	width: 100%;
	border-collapse: collapse;
}

.order-items-table th,
.order-items-table td
{
	padding: 10px;
	border: 1px solid #ddd;
	text-align: left;
}

.order-items-table th
{
	background-color: #f5f5f5;
}

.product-thumbnail
{
	width: 50px;
	height: 50px;
	object-fit: cover;
	border-radius: 8px;
}

.variants-list
{
	display: flex;
	flex-wrap: wrap;
}

.variant-tag
{
	background-color: #ddd;
	padding: 2px 5px;
	border-radius: 4px;
	margin-right: 5px;
	margin-bottom: 5px;
	font-size: 12px;
}

.total-row
{
	font-weight: bold;
}

.history-timeline
{
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.history-item
{
	display: flex;
	align-items: flex-start;
}

.history-dot
{
	width: 10px;
	height: 10px;
	background-color: #4caf50;
	border-radius: 50%;
	margin-right: 10px;
	margin-top: 5px;
}

.history-content
{
	flex: 1;
}

.history-status
{
	font-weight: bold;
}

.history-date
{
	font-size: 12px;
	color: #888;
}

.history-note
{
	margin-top: 5px;
	font-size: 14px;
}

.note-content
{
	background-color: #f5f5f5;
	padding: 10px;
	border-radius: 8px;
	border: 1px solid #ddd;
}
</style>