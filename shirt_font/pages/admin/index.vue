<template>
    <AdminLayout>
        <div class="dashboard">
            <h1>แดชบอร์ด</h1>

            <div class="stats-cards">
                <div class="stat-card">
                    <div class="stat-icon users">👤</div>
                    <div class="stat-content">
                        <h3>ผู้ใช้งานทั้งหมด</h3>
                        <div class="stat-value">{{ stats.users }}</div>
                        <div class="stat-change positive">+5.2% จากเดือนที่แล้ว</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon products">👕</div>
                    <div class="stat-content">
                        <h3>สินค้าทั้งหมด</h3>
                        <div class="stat-value">{{ stats.products }}</div>
                        <div class="stat-change positive">+12 สินค้าใหม่</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon orders">📦</div>
                    <div class="stat-content">
                        <h3>คำสั่งซื้อใหม่</h3>
                        <div class="stat-value">{{ stats.orders }}</div>
                        <div class="stat-change positive">+8.3% จากเดือนที่แล้ว</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon revenue">💰</div>
                    <div class="stat-content">
                        <h3>รายได้เดือนนี้</h3>
                        <div class="stat-value">฿{{ formatNumber(stats.revenue) }}</div>
                        <div class="stat-change positive">+12.7% จากเดือนที่แล้ว</div>
                    </div>
                </div>
            </div>

            <div class="dashboard-grid">
                <div class="dashboard-card chart-card">
                    <div class="card-header">
                        <h3>ยอดขายทั้งหมด</h3>
                        <div class="card-actions">
                            <select>
                                <option>7 วันล่าสุด</option>
                                <option>30 วันล่าสุด</option>
                                <option>ปีนี้</option>
                            </select>
                        </div>
                    </div>
                    <div class="chart-placeholder">
                        <!-- In a real app, you'd use a chart library here -->
                        <div class="placeholder-chart">
                            <div class="chart-bar" v-for="(value, index) in [60, 45, 80, 55, 70, 65, 90]" :key="index"
                                :style="{ height: value + 'px' }"></div>
                        </div>
                    </div>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <h3>คำสั่งซื้อล่าสุด</h3>
                        <button class="view-all">ดูทั้งหมด</button>
                    </div>

                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>เลขที่</th>
                                <th>ลูกค้า</th>
                                <th>สถานะ</th>
                                <th>ยอดรวม</th>
                                <th>วันที่</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="order in recentOrders" :key="order.id">
                                <td>#{{ order.id }}</td>
                                <td>{{ order.customer }}</td>
                                <td>
                                    <span class="status" :class="order.statusClass">{{ order.status }}</span>
                                </td>
                                <td>฿{{ order.total }}</td>
                                <td>{{ order.date }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <h3>สินค้าขายดี</h3>
                        <button class="view-all">ดูทั้งหมด</button>
                    </div>

                    <ul class="top-products">
                        <li v-for="product in topProducts" :key="product.id" class="product-item">
                            <div class="product-image">
                                <img :src="product.image" :alt="product.name" />
                            </div>
                            <div class="product-info">
                                <div class="product-name">{{ product.name }}</div>
                                <div class="product-meta">ขายแล้ว {{ product.sold }} ชิ้น</div>
                            </div>
                            <div class="product-price">฿{{ product.price }}</div>
                        </li>
                    </ul>
                </div>

                <div class="dashboard-card">
                    <div class="card-header">
                        <h3>รีวิวล่าสุด</h3>
                        <button class="view-all">ดูทั้งหมด</button>
                    </div>

                    <ul class="recent-reviews">
                        <li v-for="review in recentReviews" :key="review.id" class="review-item">
                            <div class="review-header">
                                <div class="reviewer-info">
                                    <div class="reviewer-avatar">{{ review.user.charAt(0) }}</div>
                                    <div class="reviewer-name">{{ review.user }}</div>
                                </div>
                                <div class="review-rating">
                                    <span v-for="i in 5" :key="i" class="star"
                                        :class="{ filled: i <= review.rating }">★</span>
                                </div>
                            </div>
                            <div class="review-product">สินค้า: {{ review.product }}</div>
                            <div class="review-text">{{ review.text }}</div>
                            <div class="review-date">{{ review.date }}</div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script>
import AdminLayout from '~/components/admin/AdminLayout.vue';

export default {
    components: {
        AdminLayout
    },
    data() {
        return {
            stats: {
                users: 1250,
                products: 345,
                orders: 82,
                revenue: 145700
            },
            recentOrders: [
                { id: '8752', customer: 'นายสมชาย ใจดี', status: 'จัดส่งแล้ว', statusClass: 'delivered', total: '3,450', date: '12/04/2023' },
                { id: '8751', customer: 'นางสาวสมหญิง รักเรียน', status: 'รอการชำระเงิน', statusClass: 'pending', total: '1,290', date: '12/04/2023' },
                { id: '8750', customer: 'นายสมศักดิ์ มานะ', status: 'รอการจัดส่ง', statusClass: 'processing', total: '5,900', date: '11/04/2023' },
                { id: '8749', customer: 'นางนิภา สุขใจ', status: 'จัดส่งแล้ว', statusClass: 'delivered', total: '2,750', date: '11/04/2023' },
                { id: '8748', customer: 'นายวิชัย เก่งกล้า', status: 'ยกเลิก', statusClass: 'cancelled', total: '3,200', date: '10/04/2023' }
            ],
            topProducts: [
                { id: 1, name: 'เสื้อฟุตบอลแมนยู 2023', sold: 152, price: '1,500', image: 'https://via.placeholder.com/50' },
                { id: 2, name: 'เสื้อฟุตบอลลิเวอร์พูล 2023', sold: 143, price: '1,500', image: 'https://via.placeholder.com/50' },
                { id: 3, name: 'เสื้อฟุตบอลเชลซี 2023', sold: 97, price: '1,500', image: 'https://via.placeholder.com/50' },
                { id: 4, name: 'เสื้อฟุตบอลอาร์เซนอล 2023', sold: 89, price: '1,500', image: 'https://via.placeholder.com/50' }
            ],
            recentReviews: [
                { id: 1, user: 'สมชาย ใจดี', rating: 5, product: 'เสื้อฟุตบอลแมนยู 2023', text: 'สินค้าคุณภาพดีมาก ใส่สบาย', date: '12/04/2023' },
                { id: 2, user: 'สมหญิง รักเรียน', rating: 4, product: 'เสื้อฟุตบอลลิเวอร์พูล 2023', text: 'ของแท้ สวยมาก', date: '11/04/2023' },
                { id: 3, user: 'วิชัย เก่งกล้า', rating: 3, product: 'เสื้อฟุตบอลเชลซี 2023', text: 'ใส่สบายดี แต่สีซีดเร็วไปหน่อย', date: '10/04/2023' }
            ]
        };
    },
    methods: {
        formatNumber(num) {
            return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        }
    }
};
</script>

<style scoped>
.dashboard
{
    width: 100%;
}

h1
{
    margin-bottom: 20px;
    color: #2c3e50;
}

.stats-cards
{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 20px;
}

.stat-card
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    display: flex;
    align-items: center;
}

.stat-icon
{
    width: 60px;
    height: 60px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    margin-right: 15px;
}

.stat-icon.users
{
    background-color: #3498db1a;
    color: #3498db;
}

.stat-icon.products
{
    background-color: #9b59b61a;
    color: #9b59b6;
}

.stat-icon.orders
{
    background-color: #e67e221a;
    color: #e67e22;
}

.stat-icon.revenue
{
    background-color: #2ecc711a;
    color: #2ecc71;
}

.stat-content
{
    flex-grow: 1;
}

.stat-content h3
{
    margin: 0 0 5px 0;
    font-size: 14px;
    color: #7f8c8d;
}

.stat-value
{
    font-size: 24px;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 5px;
}

.stat-change
{
    font-size: 12px;
}

.stat-change.positive
{
    color: #2ecc71;
}

.stat-change.negative
{
    color: #e74c3c;
}

.dashboard-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-gap: 20px;
}

.dashboard-card
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    overflow: hidden;
}

.chart-card
{
    grid-column: span 2;
}

.card-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.card-header h3
{
    margin: 0;
    color: #2c3e50;
}

.view-all
{
    background: none;
    border: 1px solid #3498db;
    color: #3498db;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
}

.view-all:hover
{
    background: #3498db;
    color: white;
}

.card-actions select
{
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.chart-placeholder
{
    height: 200px;
    display: flex;
    align-items: flex-end;
    padding: 20px 0;
}

.placeholder-chart
{
    width: 100%;
    display: flex;
    justify-content: space-around;
    align-items: flex-end;
    height: 100%;
}

.chart-bar
{
    width: 40px;
    background: linear-gradient(to top, #3498db, #3498dbaa);
    border-radius: 4px 4px 0 0;
    transition: height 0.5s;
}

.data-table
{
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td
{
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

.data-table th
{
    font-weight: 600;
    color: #7f8c8d;
}

.status
{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 12px;
}

.status.pending
{
    background-color: #f39c121a;
    color: #f39c12;
}

.status.processing
{
    background-color: #3498db1a;
    color: #3498db;
}

.status.delivered
{
    background-color: #2ecc711a;
    color: #2ecc71;
}

.status.cancelled
{
    background-color: #e74c3c1a;
    color: #e74c3c;
}

.top-products
{
    list-style: none;
    padding: 0;
    margin: 0;
}

.product-item
{
    display: flex;
    padding: 12px 0;
    border-bottom: 1px solid #eee;
    align-items: center;
}

.product-image
{
    width: 50px;
    height: 50px;
    background-color: #f5f5f5;
    border-radius: 4px;
    overflow: hidden;
    margin-right: 15px;
}

.product-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.product-info
{
    flex-grow: 1;
}

.product-name
{
    font-weight: 500;
    margin-bottom: 5px;
}

.product-meta
{
    font-size: 12px;
    color: #7f8c8d;
}

.product-price
{
    font-weight: 600;
    color: #e74c3c;
}

.recent-reviews
{
    list-style: none;
    padding: 0;
    margin: 0;
}

.review-item
{
    padding: 15px 0;
    border-bottom: 1px solid #eee;
}

.review-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.reviewer-info
{
    display: flex;
    align-items: center;
}

.reviewer-avatar
{
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #3498db;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    margin-right: 8px;
    font-size: 12px;
}

.reviewer-name
{
    font-weight: 500;
}

.review-rating .star
{
    color: #ddd;
    font-size: 14px;
}

.review-rating .star.filled
{
    color: #f39c12;
}

.review-product
{
    font-size: 13px;
    color: #7f8c8d;
    margin-bottom: 8px;
}

.review-text
{
    margin-bottom: 8px;
    line-height: 1.4;
}

.review-date
{
    font-size: 12px;
    color: #95a5a6;
}

@media (max-width: 1024px)
{
    .stats-cards
    {
        grid-template-columns: repeat(2, 1fr);
    }

    .dashboard-grid
    {
        grid-template-columns: 1fr;
    }

    .chart-card
    {
        grid-column: span 1;
    }
}

@media (max-width: 600px)
{
    .stats-cards
    {
        grid-template-columns: 1fr;
    }
}
</style>
