<template>
    <div class="cart-page">
        <div class="container">
            <h1>ตะกร้าสินค้า</h1>

            <div v-if="cartItems.length === 0" class="empty-cart">
                <div class="empty-cart-icon">🛒</div>
                <h2>ตะกร้าสินค้าว่างเปล่า</h2>
                <p>คุณยังไม่มีสินค้าในตะกร้า</p>
                <button class="btn btn-primary" @click="$router.push('/')">
                    เลือกซื้อสินค้า
                </button>
            </div>

            <div v-else class="cart-container">
                <div class="cart-items">
                    <div class="cart-header">
                        <div class="column product-info">สินค้า</div>
                        <div class="column price">ราคาต่อชิ้น</div>
                        <div class="column quantity">จำนวน</div>
                        <div class="column total">รวม</div>
                        <div class="column action"></div>
                    </div>

                    <div v-for="(item, index) in cartItems" :key="index" class="cart-item">
                        <div class="column product-info">
                            <div class="product-image">
                                <img :src="item.image" :alt="item.name">
                            </div>
                            <div class="product-details">
                                <h3>{{ item.name }}</h3>
                                <div class="variant-details">
                                    <span v-if="item.size" class="variant-tag">ขนาด: {{ item.size }}</span>
                                    <span v-if="item.color" class="variant-tag">สี: {{ item.color }}</span>
                                </div>
                                <p class="product-id">#{{ item.id }}</p>
                            </div>
                        </div>

                        <div class="column price">
                            ฿{{ item.price }}
                        </div>

                        <div class="column quantity">
                            <div class="quantity-control">
                                <button @click="updateQuantity(index, -1)" :disabled="item.quantity <= 1">-</button>
                                <input type="number" v-model.number="item.quantity" min="1" :max="item.stock"
                                    @change="validateQuantity(index)">
                                <button @click="updateQuantity(index, 1)"
                                    :disabled="item.quantity >= item.stock">+</button>
                            </div>
                            <div class="stock-info">คงเหลือ: {{ item.stock }} ชิ้น</div>
                        </div>

                        <div class="column total">
                            ฿{{ item.price * item.quantity }}
                        </div>

                        <div class="column action">
                            <button class="remove-button" @click="removeItem(index)">
                                ×
                            </button>
                        </div>
                    </div>
                </div>

                <div class="cart-summary">
                    <h2>สรุปคำสั่งซื้อ</h2>

                    <div class="summary-row">
                        <span>จำนวนสินค้า</span>
                        <span>{{ totalItems }} ชิ้น</span>
                    </div>

                    <div class="summary-row">
                        <span>ยอดรวม</span>
                        <span>฿{{ subtotal }}</span>
                    </div>

                    <div class="summary-row">
                        <span>ค่าจัดส่ง</span>
                        <span>฿{{ shipping }}</span>
                    </div>

                    <div class="coupon-section">
                        <input type="text" v-model="couponCode" placeholder="รหัสส่วนลด">
                        <button @click="applyCoupon">ใช้</button>
                    </div>

                    <div class="summary-row discount" v-if="discount > 0">
                        <span>ส่วนลด</span>
                        <span>-฿{{ discount }}</span>
                    </div>

                    <div class="summary-row total">
                        <span>ยอดรวมทั้งสิ้น</span>
                        <span>฿{{ total }}</span>
                    </div>

                    <button class="checkout-button" @click="checkout">
                        ดำเนินการชำระเงิน
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            cartItems: [],
            shipping: 50,
            discount: 0,
            couponCode: ''
        };
    },
    computed: {
        subtotal() {
            return this.cartItems.reduce((total, item) => {
                return total + (item.price * item.quantity);
            }, 0);
        },
        total() {
            return this.subtotal + this.shipping - this.discount;
        },
        totalItems() {
            return this.cartItems.reduce((sum, item) => sum + item.quantity, 0);
        }
    },
    mounted() {
        this.loadCartItems();
    },
    methods: {
        loadCartItems() {
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            this.cartItems = cart;
        },
        updateQuantity(index, change) {
            const newQuantity = this.cartItems[index].quantity + change;
            const maxStock = this.cartItems[index].stock;

            if (newQuantity > 0 && newQuantity <= maxStock) {
                this.cartItems[index].quantity = newQuantity;
                this.saveCart();
            }
        },
        validateQuantity(index) {
            const item = this.cartItems[index];
            if (item.quantity <= 0 || isNaN(item.quantity)) {
                item.quantity = 1;
            } else if (item.quantity > item.stock) {
                item.quantity = item.stock;
            } else {
                item.quantity = Math.floor(item.quantity);
            }
            this.saveCart();
        },
        removeItem(index) {
            this.cartItems.splice(index, 1);
            this.saveCart();
        },
        saveCart() {
            localStorage.setItem('cart', JSON.stringify(this.cartItems));
        },
        applyCoupon() {
            if (this.couponCode.toUpperCase() === 'SAVE10') {
                this.discount = Math.round(this.subtotal * 0.1);
                alert('คูปองถูกใช้งานแล้ว!');
            } else {
                alert('รหัสคูปองไม่ถูกต้อง');
            }
        },
        checkout() {
            // In a real app, you'd proceed to checkout
            this.$router.push('/checkout');
        }
    }
};
</script>

<style scoped>
.cart-page
{
    padding: 40px 0;
    background-color: #f8f8f8;
    min-height: calc(100vh - 60px);
}

h1
{
    margin-bottom: 30px;
    text-align: center;
}

.container
{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

.empty-cart
{
    text-align: center;
    padding: 60px 0;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.empty-cart-icon
{
    font-size: 60px;
    margin-bottom: 20px;
    color: #ddd;
}

.empty-cart h2
{
    font-size: 24px;
    margin-bottom: 15px;
    color: #333;
}

.empty-cart p
{
    color: #666;
    margin-bottom: 25px;
}

.btn-primary
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.cart-container
{
    display: grid;
    grid-template-columns: 1fr 350px;
    gap: 30px;
}

.cart-items
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.cart-header
{
    display: grid;
    grid-template-columns: 3fr 1fr 1fr 1fr 50px;
    background: #f8f8f8;
    padding: 15px;
    font-weight: bold;
}

.cart-item
{
    display: grid;
    grid-template-columns: 3fr 1fr 1fr 1fr 50px;
    padding: 15px;
    border-top: 1px solid #eee;
    align-items: center;
}

.product-info
{
    display: flex;
    align-items: center;
}

.product-image img
{
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
}

.product-details
{
    margin-left: 15px;
}

.product-details h3
{
    margin: 0 0 5px 0;
    font-size: 16px;
}

.variant-details
{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 5px;
}

.variant-tag
{
    display: inline-block;
    padding: 3px 8px;
    font-size: 12px;
    color: #666;
    background: #f5f5f5;
    border-radius: 2px;
}

.product-id
{
    color: #999;
    font-size: 12px;
    margin: 0;
}

.quantity-control
{
    display: flex;
    align-items: center;
    max-width: 120px;
}

.quantity-control button
{
    width: 30px;
    height: 30px;
    border: 1px solid #ddd;
    background: #f8f8f8;
    font-size: 16px;
    cursor: pointer;
}

.quantity-control input
{
    width: 40px;
    height: 30px;
    border: 1px solid #ddd;
    text-align: center;
    margin: 0 5px;
}

.stock-info
{
    font-size: 12px;
    color: #666;
    margin-top: 5px;
}

.remove-button
{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 1px solid #ddd;
    background: white;
    color: #999;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.cart-summary
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
    padding: 20px;
    position: sticky;
    top: 20px;
}

.cart-summary h2
{
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 1px solid #eee;
}

.summary-row
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}

.summary-row.discount
{
    color: #ee4d2d;
}

.summary-row.total
{
    font-weight: bold;
    font-size: 18px;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #eee;
}

.coupon-section
{
    display: flex;
    margin: 15px 0;
}

.coupon-section input
{
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
}

.coupon-section button
{
    padding: 10px 15px;
    background: #f8f8f8;
    border: 1px solid #ddd;
    border-left: none;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
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
    margin-top: 15px;
    cursor: pointer;
}

.checkout-button:hover
{
    background-color: #d73211;
}

@media (max-width: 992px)
{
    .cart-container
    {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px)
{
    .cart-header
    {
        display: none;
    }

    .cart-item
    {
        grid-template-columns: 1fr;
        gap: 10px;
    }

    .column
    {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .column.product-info
    {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }

    .column.product-info:before
    {
        content: 'สินค้า';
        font-weight: bold;
    }

    .column.price:before
    {
        content: 'ราคาต่อชิ้น';
        font-weight: bold;
    }

    .column.quantity:before
    {
        content: 'จำนวน';
        font-weight: bold;
    }

    .column.total:before
    {
        content: 'รวม';
        font-weight: bold;
    }

    .column.action
    {
        justify-content: flex-end;
    }
}
</style>
