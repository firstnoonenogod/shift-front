<template>
    <div class="order-success">
        <div class="container">
            <div class="success-card">
                <div class="success-icon">
                    <span>✓</span>
                </div>
                <h1>การสั่งซื้อสำเร็จ</h1>
                <p>ขอบคุณสำหรับการสั่งซื้อ</p>
                <p class="order-number">หมายเลขคำสั่งซื้อ: #{{ orderId }}</p>

                <div class="order-summary">
                    <h3>สรุปคำสั่งซื้อ</h3>
                    <div class="summary-item">
                        <span>จำนวนสินค้า:</span>
                        <span>{{ itemCount }} ชิ้น</span>
                    </div>
                    <div class="summary-item">
                        <span>ยอดรวม:</span>
                        <span>฿{{ formatPrice(totalAmount) }}</span>
                    </div>
                </div>

                <div class="action-buttons">
                    <button class="btn btn-primary" @click="$router.push('/')">
                        กลับไปหน้าหลัก
                    </button>
                    <button class="btn btn-secondary" @click="$router.push('/orders')">
                        ดูรายการคำสั่งซื้อ
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
            orderId: '',
            itemCount: 0,
            totalAmount: 0
        };
    },
    mounted() {
        // Get data from URL query parameters
        if (this.$route.query.orderId) {
            this.orderId = this.$route.query.orderId;
            this.itemCount = parseInt(this.$route.query.itemCount || 0);
            this.totalAmount = parseFloat(this.$route.query.totalAmount || 0);
        } else {
            // Fallback to random data if no query params
            this.orderId = 'ORDER' + Math.floor(100000 + Math.random() * 900000);
            this.itemCount = Math.floor(1 + Math.random() * 5);
            this.totalAmount = Math.floor(500 + Math.random() * 2000);
        }
    },
    methods: {
        formatPrice(price) {
            return new Intl.NumberFormat('th-TH').format(price);
        }
    }
};
</script>

<style scoped>
.order-success
{
    min-height: 100vh;
    padding: 40px 0;
    background-color: #f8f8f8;
}

.success-card
{
    max-width: 600px;
    margin: 0 auto;
    padding: 40px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.success-icon
{
    width: 80px;
    height: 80px;
    margin: 0 auto 20px;
    background: #4CAF50;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.success-icon span
{
    color: white;
    font-size: 40px;
    font-weight: bold;
}

h1
{
    color: #333;
    margin-bottom: 10px;
}

.order-number
{
    font-weight: bold;
    margin: 20px 0;
    font-size: 18px;
}

.order-summary
{
    margin: 30px 0;
    text-align: left;
    border-top: 1px solid #eee;
    padding-top: 20px;
}

.summary-item
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}

.action-buttons
{
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-top: 30px;
}

.btn-secondary
{
    background-color: #fff;
    border: 1px solid #ddd;
    color: #333;
}

.btn-secondary:hover
{
    background-color: #f5f5f5;
}
</style>
