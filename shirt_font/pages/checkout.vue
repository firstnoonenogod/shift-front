<template>
    <div class="checkout-page">
        <div class="container">
            <h1>ชำระเงิน</h1>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังดำเนินการ...</p>
            </div>

            <div v-else-if="orderSuccess" class="success-container">
                <div class="success-icon">✓</div>
                <h2>สั่งซื้อสำเร็จ!</h2>
                <p>หมายเลขคำสั่งซื้อ: {{ orderNumber }}</p>
                <p>ขอบคุณสำหรับการสั่งซื้อ</p>
                <button class="primary-button" @click="goToOrderSuccess">
                    ดูรายละเอียดคำสั่งซื้อ
                </button>
                <button class="secondary-button" @click="$router.push('/')">
                    กลับสู่หน้าหลัก
                </button>
            </div>

            <div v-else-if="error" class="error-container">
                <div class="error-icon">!</div>
                <h2>เกิดข้อผิดพลาด</h2>
                <p>{{ error }}</p>
                <button class="primary-button" @click="retryOrder">
                    ลองอีกครั้ง
                </button>
            </div>

            <div v-else class="checkout-container">
                <!-- Order Summary -->
                <div class="order-summary">
                    <h2>สรุปรายการสั่งซื้อ</h2>

                    <div class="cart-items">
                        <div v-for="(item, index) in cartItems" :key="index" class="cart-item">
                            <div class="item-image">
                                <img :src="item.image" :alt="item.name" />
                            </div>
                            <div class="item-details">
                                <h3 class="item-name">{{ item.name }}</h3>
                                <div class="item-variants">
                                    <span v-if="item.size" class="variant-tag">ขนาด: {{ item.size }}</span>
                                    <span v-if="item.color" class="variant-tag">สี: {{ item.color }}</span>
                                </div>
                                <div class="item-price">฿{{ item.price }} × {{ item.quantity }}</div>
                            </div>
                            <div class="item-total">
                                ฿{{ item.price * item.quantity }}
                            </div>
                        </div>
                    </div>

                    <div class="summary-totals">
                        <div class="summary-row">
                            <span>ยอดรวม</span>
                            <span>฿{{ subtotal }}</span>
                        </div>
                        <div class="summary-row">
                            <span>ค่าจัดส่ง</span>
                            <span>฿{{ shipping }}</span>
                        </div>
                        <div class="summary-row total">
                            <span>รวมทั้งสิ้น</span>
                            <span>฿{{ total }}</span>
                        </div>
                    </div>
                </div>

                <!-- Shipping Information -->
                <div class="shipping-section">
                    <h2>ที่อยู่จัดส่ง</h2>

                    <form @submit.prevent="submitOrder" class="shipping-form">
                        <div class="form-group">
                            <label for="fullName">ชื่อ-นามสกุล*</label>
                            <input type="text" id="fullName" v-model="shippingInfo.fullName" required
                                placeholder="กรุณากรอกชื่อ-นามสกุลผู้รับ" />
                        </div>

                        <div class="form-group">
                            <label for="phone">เบอร์โทรศัพท์*</label>
                            <input type="tel" id="phone" v-model="shippingInfo.phone" required
                                placeholder="กรุณากรอกเบอร์โทรศัพท์" />
                        </div>

                        <div class="form-group">
                            <label for="address">ที่อยู่*</label>
                            <textarea id="address" v-model="shippingInfo.address" required
                                placeholder="กรุณากรอกที่อยู่จัดส่ง" rows="3"></textarea>
                        </div>

                        <div class="form-row">
                            <div class="form-group">
                                <label for="province">จังหวัด*</label>
                                <select id="province" v-model="shippingInfo.province" required>
                                    <option value="" disabled>เลือกจังหวัด</option>
                                    <option value="กรุงเทพมหานคร">กรุงเทพมหานคร</option>
                                    <option value="เชียงใหม่">เชียงใหม่</option>
                                    <option value="ขอนแก่น">ขอนแก่น</option>
                                    <option value="ชลบุรี">ชลบุรี</option>
                                    <option value="ภูเก็ต">ภูเก็ต</option>
                                    <!-- Add more provinces as needed -->
                                </select>
                            </div>

                            <div class="form-group">
                                <label for="postalCode">รหัสไปรษณีย์*</label>
                                <input type="text" id="postalCode" v-model="shippingInfo.postalCode" required
                                    placeholder="รหัสไปรษณีย์" />
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="notes">หมายเหตุ</label>
                            <textarea id="notes" v-model="shippingInfo.notes" placeholder="หมายเหตุเพิ่มเติม (ถ้ามี)"
                                rows="2"></textarea>
                        </div>

                        <h2>วิธีการชำระเงิน</h2>

                        <div class="payment-methods">
                            <div v-for="method in paymentMethods" :key="method.id" class="payment-method"
                                :class="{ active: selectedPaymentMethod === method.id }"
                                @click="selectedPaymentMethod = method.id">
                                <div class="method-radio">
                                    <div class="radio-inner" v-if="selectedPaymentMethod === method.id"></div>
                                </div>
                                <div class="method-icon">{{ method.icon }}</div>
                                <div class="method-details">
                                    <div class="method-name">{{ method.name }}</div>
                                    <div class="method-description">{{ method.description }}</div>
                                </div>
                            </div>
                        </div>

                        <button type="submit" class="checkout-button" :disabled="loading || !isFormValid">
                            ชำระเงิน ฿{{ total }}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import useOrder from '~/composables/useOrder';
import usePayment from '~/composables/usePayment';

export default {
    data() {
        return {
            cartItems: [],
            loading: false,
            error: null,
            orderSuccess: false,
            orderNumber: '',
            orderId: '',
            shipping: 50,
            shippingInfo: {
                fullName: '',
                phone: '',
                address: '',
                province: '',
                postalCode: '',
                notes: ''
            },
            selectedPaymentMethod: 'cod',
            paymentMethods: [
                {
                    id: 'cod',
                    name: 'เก็บเงินปลายทาง',
                    description: 'จ่ายตอนได้รับสินค้า',
                    icon: '💵'
                },
                {
                    id: 'bank_transfer',
                    name: 'โอนผ่านธนาคาร',
                    description: 'โอนเงินผ่านบัญชีธนาคาร',
                    icon: '🏦'
                },
                {
                    id: 'credit_card',
                    name: 'บัตรเครดิต/เดบิต',
                    description: 'Visa, Mastercard, JCB',
                    icon: '💳'
                }
            ],
            userId: 'guest' // Default guest user
        };
    },
    setup() {
        const { createOrder } = useOrder();
        const { createPayment } = usePayment();

        return {
            createOrder,
            createPayment
        };
    },
    computed: {
        subtotal() {
            return this.cartItems.reduce((total, item) => {
                return total + item.price * item.quantity;
            }, 0);
        },
        total() {
            return this.subtotal + this.shipping;
        },
        isFormValid() {
            const { fullName, phone, address, province, postalCode } = this.shippingInfo;
            return fullName && phone && address && province && postalCode;
        }
    },
    mounted() {
        this.loadCartItems();
    },
    methods: {
        loadCartItems() {
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            if (cart.length === 0) {
                // Redirect to cart page if no items
                this.$router.push('/cart');
                return;
            }
            this.cartItems = cart;
        },

        formatShippingAddress() {
            const { fullName, phone, address, province, postalCode, notes } = this.shippingInfo;

            let formattedAddress = `${fullName}, ${phone}, ${address}, ${province} ${postalCode}`;
            if (notes) {
                formattedAddress += ` (${notes})`;
            }

            return formattedAddress;
        },

        async submitOrder() {
            if (!this.isFormValid) return;

            this.loading = true;
            this.error = null;

            try {
                console.log('Starting order submission process...');

                // Format the order data according to API requirements
                const orderData = {
                    items: this.cartItems.map(item => ({
                        product_id: item.id,
                        variant_id: item.variant_id || null,
                        quantity: item.quantity
                    })),
                    shipping_address: this.formatShippingAddress(),
                    user_id: this.userId !== 'guest' ? this.userId : null
                };

                console.log('Prepared order data:', orderData);

                // Create order using the API
                const orderResponse = await this.createOrder(orderData);
                console.log('Order created successfully:', orderResponse);

                this.orderId = orderResponse.id;
                this.orderNumber = `ORD-${this.orderId.substring(0, 6)}`;

                // Create payment record
                const paymentData = {
                    order_id: this.orderId,
                    amount: this.total,
                    payment_method: this.selectedPaymentMethod,
                    status: this.selectedPaymentMethod === 'cod' ? 'pending' : 'completed'
                };

                console.log('Creating payment with data:', paymentData);
                const paymentResponse = await this.createPayment(paymentData);
                console.log('Payment created successfully:', paymentResponse);

                // Clear the cart
                localStorage.removeItem('cart');

                // Show success message
                this.orderSuccess = true;

            } catch (error) {
                console.error('Error submitting order:', error);

                let errorMessage = 'เกิดข้อผิดพลาดในการสั่งซื้อ กรุณาลองใหม่อีกครั้ง';

                if (error.response) {
                    console.error('Error response data:', error.response.data);
                    errorMessage += ` (${error.response.status}: ${error.response.data?.detail || error.response.statusText})`;
                } else if (error.request) {
                    console.error('No response received:', error.request);
                    errorMessage += ' (ไม่ได้รับการตอบกลับจากเซิร์ฟเวอร์)';
                } else {
                    errorMessage += ` (${error.message})`;
                }

                this.error = errorMessage;
            } finally {
                this.loading = false;
            }
        },

        async updateProductStocks() {
            try {
                // Process each cart item to update stock
                const updatePromises = this.cartItems.map(async (item) => {
                    try {
                        // First, get the current product data to ensure we have the latest stock count
                        const productResponse = await axios.get(`http://127.0.0.1:8000/products/${item.id}`);
                        const product = productResponse.data;

                        console.log(`Current product data for ${item.name}:`, product);
                        console.log(`Current stock: ${product.stock}, Order quantity: ${item.quantity}`);

                        // Calculate new stock by subtracting purchased quantity
                        const newStock = Math.max(0, product.stock - item.quantity);

                        // Prepare update data with all required fields
                        const updateData = {
                            name: product.name,
                            description: product.description,
                            price: product.price,
                            stock: newStock,
                            category_id: product.category_id,
                            images: product.images || []
                        };

                        // Send PUT request to update the product
                        console.log(`Updating stock for ${product.name} from ${product.stock} to ${newStock}`);
                        await axios.put(`http://127.0.0.1:8000/products/${item.id}`, updateData);
                        console.log(`✅ Stock updated successfully for ${product.name}`);

                    } catch (error) {
                        console.error(`Failed to update stock for product ${item.id}:`, error);
                        throw error;
                    }
                });

                // Wait for all stock updates to complete
                await Promise.all(updatePromises);
                console.log('All product stocks updated successfully');

            } catch (error) {
                console.error('Error updating product stocks:', error);
                throw new Error('Failed to update product stocks');
            }
        },

        retryOrder() {
            this.error = null;
        },

        goToOrderSuccess() {
            this.$router.push({
                path: '/order-success',
                query: {
                    orderId: this.orderNumber,
                    itemCount: this.cartItems.length,
                    totalAmount: this.total
                }
            });
        }
    }
};
</script>

<style scoped>
.checkout-page
{
    background-color: #f8f8f8;
    padding: 40px 0;
    min-height: 100vh;
}

.container
{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

h1
{
    text-align: center;
    margin-bottom: 30px;
    color: #333;
}

.loading-container,
.success-container,
.error-container
{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 60px 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin: 0 auto;
    max-width: 600px;
}

.loading-spinner
{
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #ee4d2d;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
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

.success-icon,
.error-icon
{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    margin-bottom: 20px;
}

.success-icon
{
    background-color: #52c41a;
    color: white;
}

.error-icon
{
    background-color: #ff4d4f;
    color: white;
}

.success-container h2,
.error-container h2
{
    margin: 0 0 15px;
    color: #333;
}

.primary-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: all 0.2s;
}

.primary-button:hover
{
    background-color: #d73211;
}

.secondary-button
{
    background-color: #ccc;
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: all 0.2s;
}

.secondary-button:hover
{
    background-color: #999;
}

.checkout-container
{
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 30px;
}

.order-summary
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 25px;
    align-self: flex-start;
}

.order-summary h2
{
    margin: 0 0 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #f0f0f0;
    color: #333;
    font-size: 20px;
}

.cart-items
{
    margin-bottom: 20px;
}

.cart-item
{
    display: flex;
    padding: 15px 0;
    border-bottom: 1px solid #f0f0f0;
}

.cart-item:last-child
{
    border-bottom: none;
}

.item-image
{
    width: 80px;
    min-width: 80px;
    height: 80px;
    margin-right: 15px;
}

.item-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
}

.item-details
{
    flex-grow: 1;
}

.item-name
{
    margin: 0 0 5px;
    font-size: 16px;
    color: #333;
}

.item-variants
{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}

.variant-tag
{
    background: #f5f5f5;
    color: #666;
    padding: 2px 8px;
    border-radius: 2px;
    font-size: 12px;
}

.item-price
{
    color: #666;
    font-size: 14px;
}

.item-total
{
    font-weight: 600;
    color: #ee4d2d;
    display: flex;
    align-items: center;
    margin-left: 15px;
}

.summary-totals
{
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid #f0f0f0;
}

.summary-row
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    color: #666;
}

.summary-row.total
{
    font-weight: 600;
    color: #333;
    font-size: 18px;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #f0f0f0;
}

.shipping-section
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 25px;
}

.shipping-section h2
{
    margin: 0 0 20px;
    color: #333;
    font-size: 20px;
}

.shipping-form .form-group
{
    margin-bottom: 20px;
}

.shipping-form label
{
    display: block;
    margin-bottom: 8px;
    color: #333;
    font-weight: 500;
}

.shipping-form input,
.shipping-form select,
.shipping-form textarea
{
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.shipping-form textarea
{
    resize: vertical;
}

.form-row
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.payment-methods
{
    margin: 20px 0;
}

.payment-method
{
    display: flex;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-bottom: 10px;
    cursor: pointer;
    transition: all 0.2s;
}

.payment-method:hover
{
    border-color: #ee4d2d;
}

.payment-method.active
{
    border-color: #ee4d2d;
    background-color: rgba(238, 77, 45, 0.05);
}

.method-radio
{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 2px solid #ddd;
    margin-right: 15px;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}

.payment-method.active .method-radio
{
    border-color: #ee4d2d;
}

.radio-inner
{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #ee4d2d;
}

.method-icon
{
    font-size: 24px;
    margin-right: 15px;
    display: flex;
    align-items: center;
}

.method-name
{
    font-weight: 600;
    margin-bottom: 3px;
}

.method-description
{
    font-size: 14px;
    color: #666;
}

.checkout-button
{
    width: 100%;
    padding: 15px;
    background-color: #ee4d2d;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    margin-top: 20px;
    transition: all 0.2s;
}

.checkout-button:hover
{
    background-color: #d73211;
}

.checkout-button:disabled
{
    background-color: #cccccc;
    cursor: not-allowed;
}

@media (max-width: 992px)
{
    .checkout-container
    {
        grid-template-columns: 1fr;
    }

    .order-summary
    {
        order: 1;
    }

    .shipping-section
    {
        order: 0;
    }
}
</style>
