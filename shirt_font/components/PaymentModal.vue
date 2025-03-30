<template>
    <div class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h2>ชำระเงิน</h2>
                <button class="close-button" @click="$emit('close')">×</button>
            </div>

            <div class="modal-body">
                <div class="order-summary">
                    <h3>สรุปรายการสั่งซื้อ</h3>
                    <div class="order-item">
                        <img :src="product.image" :alt="product.name" class="item-image">
                        <div class="item-details">
                            <div class="item-name">{{ product.name }}</div>
                            <div class="item-options">
                                <span>{{ selectedSize }}</span>
                                <span> | </span>
                                <span>{{ selectedColor }}</span>
                            </div>
                            <div class="item-quantity">จำนวน: {{ quantity }} ชิ้น</div>
                            <div class="item-price">฿{{ product.price * quantity }}</div>
                        </div>
                    </div>

                    <div class="order-total">
                        <div class="subtotal">
                            <span>ราคาสินค้า</span>
                            <span>฿{{ product.price * quantity }}</span>
                        </div>
                        <div class="shipping">
                            <span>ค่าจัดส่ง</span>
                            <span>฿{{ shippingFee }}</span>
                        </div>
                        <div class="total">
                            <span>ยอดรวมทั้งหมด</span>
                            <span>฿{{ totalAmount }}</span>
                        </div>
                    </div>
                </div>

                <div class="shipping-info" v-if="currentStep === 1">
                    <h3>ที่อยู่จัดส่ง</h3>
                    <div class="form-group">
                        <label>ชื่อ-นามสกุล</label>
                        <input type="text" v-model="shippingDetails.name" placeholder="กรุณากรอกชื่อ-นามสกุล">
                    </div>
                    <div class="form-group">
                        <label>เบอร์โทรศัพท์</label>
                        <input type="tel" v-model="shippingDetails.phone" placeholder="กรุณากรอกเบอร์โทรศัพท์">
                    </div>
                    <div class="form-group">
                        <label>ที่อยู่</label>
                        <textarea v-model="shippingDetails.address" placeholder="บ้านเลขที่, ถนน, ตำบล/แขวง"></textarea>
                    </div>
                    <div class="form-group">
                        <label>จังหวัด</label>
                        <select v-model="shippingDetails.province">
                            <option value="">กรุณาเลือกจังหวัด</option>
                            <option value="กรุงเทพมหานคร">กรุงเทพมหานคร</option>
                            <option value="เชียงใหม่">เชียงใหม่</option>
                            <option value="ขอนแก่น">ขอนแก่น</option>
                            <option value="ชลบุรี">ชลบุรี</option>
                            <option value="ภูเก็ต">ภูเก็ต</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>รหัสไปรษณีย์</label>
                        <input type="text" v-model="shippingDetails.postalCode" placeholder="กรุณากรอกรหัสไปรษณีย์">
                    </div>
                    <div class="form-group">
                        <button class="continue-button" @click="goToPaymentMethod" :disabled="!isShippingFormValid">
                            ดำเนินการต่อ
                        </button>
                    </div>
                </div>

                <div class="payment-method" v-if="currentStep === 2">
                    <h3>วิธีการชำระเงิน</h3>
                    <div class="payment-options">
                        <div class="payment-option" v-for="method in paymentMethods" :key="method.id"
                            :class="{ active: selectedPaymentMethod === method.id }"
                            @click="selectedPaymentMethod = method.id">
                            <img :src="method.icon" :alt="method.name" class="payment-icon">
                            <div class="payment-name">{{ method.name }}</div>
                        </div>
                    </div>

                    <div class="card-details" v-if="selectedPaymentMethod === 'credit_card'">
                        <div class="form-group">
                            <label>เลขบัตรเครดิต/เดบิต</label>
                            <input type="text" v-model="paymentDetails.cardNumber" placeholder="xxxx xxxx xxxx xxxx">
                        </div>
                        <div class="form-row">
                            <div class="form-group half">
                                <label>วันหมดอายุ</label>
                                <input type="text" v-model="paymentDetails.expiry" placeholder="MM/YY">
                            </div>
                            <div class="form-group half">
                                <label>รหัส CVV</label>
                                <input type="text" v-model="paymentDetails.cvv" placeholder="123">
                            </div>
                        </div>
                        <div class="form-group">
                            <label>ชื่อบนบัตร</label>
                            <input type="text" v-model="paymentDetails.cardName" placeholder="กรุณากรอกชื่อบนบัตร">
                        </div>
                    </div>

                    <div class="bank-transfer" v-if="selectedPaymentMethod === 'bank_transfer'">
                        <div class="bank-accounts">
                            <div class="bank-account">
                                <div class="bank-logo">🏦</div>
                                <div class="bank-info">
                                    <div>ธนาคารกสิกรไทย</div>
                                    <div>123-4-56789-0</div>
                                    <div>บริษัท ชิร์ทช็อป จำกัด</div>
                                </div>
                            </div>
                            <div class="bank-account">
                                <div class="bank-logo">🏦</div>
                                <div class="bank-info">
                                    <div>ธนาคารไทยพาณิชย์</div>
                                    <div>098-7-65432-1</div>
                                    <div>บริษัท ชิร์ทช็อป จำกัด</div>
                                </div>
                            </div>
                        </div>
                        <div class="receipt-upload">
                            <label>อัปโหลดสลิปการโอนเงิน</label>
                            <div class="upload-area">
                                <span>คลิกเพื่ออัปโหลดไฟล์</span>
                                <input type="file" @change="handleFileUpload">
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <button class="payment-button" @click="processPayment" :disabled="!isPaymentValid">
                            ชำระเงิน ฿{{ totalAmount }}
                        </button>
                        <button class="back-button" @click="currentStep = 1">
                            ย้อนกลับ
                        </button>
                    </div>
                </div>

                <!-- Order Success Message -->
                <div class="order-success" v-if="currentStep === 3">
                    <div class="success-icon">✓</div>
                    <h3>การสั่งซื้อเสร็จสมบูรณ์</h3>
                    <p>หมายเลขคำสั่งซื้อ: {{ orderNumber }}</p>
                    <p>ขอบคุณสำหรับการสั่งซื้อ</p>
                    <div class="form-group">
                        <button class="continue-shopping-button" @click="continueToShopping">
                            กลับสู่หน้าหลัก
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Review Modal after successful payment -->
        <ReviewModal v-if="showReviewModal" :product="{
            id: product.id,
            name: product.name,
            image: product.image,
            size: selectedSize,
            color: selectedColor
        }" :orderId="orderNumber" @close="closeReviewModal" @skip="closeReviewModal"
            @success="handleReviewSuccess" />
    </div>
</template>

<script>
import ReviewModal from '~/components/product/ReviewModal.vue';

export default {
    components: {
        ReviewModal
    },
    props: {
        product: {
            type: Object,
            required: true
        },
        selectedSize: {
            type: String,
            required: true
        },
        selectedColor: {
            type: String,
            required: true
        },
        quantity: {
            type: Number,
            required: true
        }
    },
    data() {
        return {
            currentStep: 1,
            shippingFee: 50,
            shippingDetails: {
                name: '',
                phone: '',
                address: '',
                province: '',
                postalCode: ''
            },
            selectedPaymentMethod: 'credit_card',
            paymentDetails: {
                cardNumber: '',
                expiry: '',
                cvv: '',
                cardName: ''
            },
            paymentMethods: [
                {
                    id: 'credit_card',
                    name: 'บัตรเครดิต / เดบิต',
                    icon: 'https://cdn.iconscout.com/icon/free/png-256/free-credit-card-2650080-2196542.png'
                },
                {
                    id: 'bank_transfer',
                    name: 'โอนเงินผ่านธนาคาร',
                    icon: 'https://cdn.iconscout.com/icon/premium/png-256-thumb/bank-transfer-2130466-1793018.png'
                },
                {
                    id: 'promptpay',
                    name: 'พร้อมเพย์',
                    icon: 'https://promptpay.io/asset/img/PromptPay-logo.jpg'
                }
            ],
            orderNumber: '',
            uploadedFile: null,
            showReviewModal: false,
            reviewSubmitted: false
        };
    },
    computed: {
        totalAmount() {
            return (this.product.price * this.quantity) + this.shippingFee;
        },
        isShippingFormValid() {
            return (
                this.shippingDetails.name &&
                this.shippingDetails.phone &&
                this.shippingDetails.address &&
                this.shippingDetails.province &&
                this.shippingDetails.postalCode
            );
        },
        isPaymentValid() {
            if (this.selectedPaymentMethod === 'credit_card') {
                return (
                    this.paymentDetails.cardNumber &&
                    this.paymentDetails.expiry &&
                    this.paymentDetails.cvv &&
                    this.paymentDetails.cardName
                );
            } else if (this.selectedPaymentMethod === 'bank_transfer') {
                return this.uploadedFile !== null;
            }
            return true;
        }
    },
    methods: {
        goToPaymentMethod() {
            if (this.isShippingFormValid) {
                this.currentStep = 2;
            }
        },
        handleFileUpload(e) {
            this.uploadedFile = e.target.files[0];
        },
        processPayment() {
            if (this.isPaymentValid) {
                // In a real app, you would send payment information to your server here
                // For this example, we'll just simulate a successful payment
                setTimeout(() => {
                    this.orderNumber = 'OD' + Date.now().toString().substring(4);
                    this.currentStep = 3;

                    // Show review modal after a short delay
                    setTimeout(() => {
                        this.showReviewModal = true;
                    }, 1500);
                }, 1500);
            }
        },

        continueToShopping() {
            // If the review modal hasn't been shown yet, show it before continuing
            if (!this.reviewSubmitted && !this.showReviewModal) {
                this.showReviewModal = true;
                return;
            }

            this.$emit('close');
            this.$router.push('/');
        },

        closeReviewModal() {
            this.showReviewModal = false;
        },

        handleReviewSuccess(reviewData) {
            this.reviewSubmitted = true;
            this.showReviewModal = false;

            // Optionally show a success message
            alert('ขอบคุณสำหรับการรีวิวสินค้า!');
        }
    }
};
</script>

<style scoped>
.modal-overlay
{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content
{
    background-color: white;
    border-radius: 8px;
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #f0f0f0;
}

.modal-header h2
{
    margin: 0;
    color: #333;
}

.close-button
{
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #999;
}

.modal-body
{
    padding: 20px;
}

.order-summary
{
    margin-bottom: 25px;
}

.order-summary h3
{
    margin-bottom: 15px;
    color: #333;
}

.order-item
{
    display: flex;
    gap: 15px;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 15px;
    margin-bottom: 15px;
}

.item-image
{
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
}

.item-details
{
    flex-grow: 1;
}

.item-name
{
    font-weight: 600;
    margin-bottom: 5px;
}

.item-options
{
    color: #666;
    font-size: 14px;
    margin-bottom: 5px;
}

.item-quantity
{
    color: #666;
    font-size: 14px;
    margin-bottom: 5px;
}

.item-price
{
    font-weight: 600;
    color: #ee4d2d;
}

.order-total
{
    padding: 15px 0;
}

.subtotal,
.shipping,
.total
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.total
{
    font-weight: 600;
    color: #ee4d2d;
    font-size: 18px;
    border-top: 1px dashed #f0f0f0;
    padding-top: 8px;
    margin-top: 8px;
}

.form-group
{
    margin-bottom: 15px;
}

.form-group label
{
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group input,
.form-group textarea,
.form-group select
{
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.form-group textarea
{
    min-height: 80px;
    resize: vertical;
}

.form-row
{
    display: flex;
    gap: 15px;
}

.half
{
    flex: 0 0 calc(50% - 8px);
}

.continue-button,
.payment-button,
.continue-shopping-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
}

.back-button
{
    background-color: #f5f5f5;
    color: #666;
    border: 1px solid #ddd;
    padding: 12px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 10px;
    width: 100%;
}

.continue-button:disabled,
.payment-button:disabled
{
    background-color: #cccccc;
    cursor: not-allowed;
}

.payment-options
{
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.payment-option
{
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 15px;
    cursor: pointer;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 10px;
}

.payment-option.active
{
    border-color: #ee4d2d;
    background-color: rgba(238, 77, 45, 0.05);
}

.payment-icon
{
    width: 32px;
    height: 32px;
    object-fit: contain;
}

.card-details,
.bank-transfer
{
    border: 1px solid #f0f0f0;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 20px;
    background-color: #fafafa;
}

.bank-accounts
{
    margin-bottom: 15px;
}

.bank-account
{
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px;
    border: 1px solid #eee;
    border-radius: 4px;
    margin-bottom: 10px;
    background-color: white;
}

.bank-logo
{
    font-size: 24px;
}

.bank-info div
{
    margin-bottom: 3px;
}

.upload-area
{
    border: 2px dashed #ddd;
    border-radius: 4px;
    padding: 20px;
    text-align: center;
    cursor: pointer;
    position: relative;
}

.upload-area input[type="file"]
{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.order-success
{
    text-align: center;
    padding: 30px 0;
}

.success-icon
{
    background-color: #4caf50;
    color: white;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    margin: 0 auto 20px;
}

.order-success h3
{
    margin-bottom: 10px;
    color: #333;
}

.order-success p
{
    color: #666;
    margin-bottom: 5px;
}
</style>