<template>
    <AdminLayout>
        <div class="dashboard-container">
            <div class="page-header">
                <h1>แดชบอร์ด</h1>
                <div class="date-selector">
                    <button class="date-button" :class="{ active: dateRange === '7days' }"
                        @click="dateRange = '7days'">7 วัน</button>
                    <button class="date-button" :class="{ active: dateRange === '30days' }"
                        @click="dateRange = '30days'">30 วัน</button>
                    <button class="date-button" :class="{ active: dateRange === 'year' }" @click="dateRange = 'year'">12
                        เดือน</button>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else>
                <!-- Summary Stats Cards -->
                <div class="stats-cards">
                    <div class="stat-card">
                        <div class="stat-header">
                            <h3>ยอดขายรวม</h3>
                            <i class="fas fa-chart-line stat-icon revenue"></i>
                        </div>
                        <div class="stat-value">฿{{ formatPrice(totalRevenue) }}</div>
                        <div class="stat-change" :class="revenueChange >= 0 ? 'positive' : 'negative'">
                            <i :class="revenueChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                            {{ Math.abs(revenueChange) }}% จากช่วงก่อนหน้า
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-header">
                            <h3>คำสั่งซื้อ</h3>
                            <i class="fas fa-shopping-cart stat-icon orders"></i>
                        </div>
                        <div class="stat-value">{{ totalOrders }}</div>
                        <div class="stat-change" :class="orderChange >= 0 ? 'positive' : 'negative'">
                            <i :class="orderChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                            {{ Math.abs(orderChange) }}% จากช่วงก่อนหน้า
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-header">
                            <h3>ลูกค้าใหม่</h3>
                            <i class="fas fa-users stat-icon users"></i>
                        </div>
                        <div class="stat-value">{{ newUsers }}</div>
                        <div class="stat-change" :class="userChange >= 0 ? 'positive' : 'negative'">
                            <i :class="userChange >= 0 ? 'fas fa-arrow-up' : 'fas fa-arrow-down'"></i>
                            {{ Math.abs(userChange) }}% จากช่วงก่อนหน้า
                        </div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-header">
                            <h3>คะแนนรีวิวเฉลี่ย</h3>
                            <i class="fas fa-star stat-icon reviews"></i>
                        </div>
                        <div class="stat-value">{{ averageRating.toFixed(1) }}</div>
                        <div class="rating-stars">
                            <i v-for="i in 5" :key="i" class="fas fa-star"
                                :class="{ filled: i <= Math.round(averageRating) }"></i>
                        </div>
                    </div>
                </div>

                <!-- Sales Chart -->
                <div class="chart-section">
                    <div class="section-header">
                        <h2>ยอดขายตามช่วงเวลา</h2>
                        <div class="section-actions">
                            <select v-model="chartType">
                                <option value="revenue">ยอดขาย</option>
                                <option value="orders">จำนวนคำสั่งซื้อ</option>
                            </select>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="salesChart" ref="salesChart"></canvas>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <!-- Recent Orders -->
                    <div class="grid-item recent-orders">
                        <div class="section-header">
                            <h2>คำสั่งซื้อล่าสุด</h2>
                            <nuxt-link to="/admin/orders" class="view-all">ดูทั้งหมด</nuxt-link>
                        </div>
                        <div class="table-container">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>รหัส</th>
                                        <th>ลูกค้า</th>
                                        <th>วันที่</th>
                                        <th>ยอดรวม</th>
                                        <th>สถานะ</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="order in recentOrders" :key="order.id" @click="navigateToOrder(order.id)"
                                        class="clickable">
                                        <td>{{ order.orderNumber }}</td>
                                        <td>{{ order.customerName }}</td>
                                        <td>{{ formatDate(order.date) }}</td>
                                        <td>฿{{ formatPrice(order.total) }}</td>
                                        <td>
                                            <span class="status-badge" :class="order.status">
                                                {{ getStatusText(order.status) }}
                                            </span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Top Products -->
                    <div class="grid-item top-products">
                        <div class="section-header">
                            <h2>สินค้าขายดี</h2>
                            <nuxt-link to="/admin/products" class="view-all">ดูทั้งหมด</nuxt-link>
                        </div>
                        <div class="product-list">
                            <div v-for="product in topProducts" :key="product.id" class="product-item">
                                <div class="product-image">
                                    <img :src="product.image || 'https://via.placeholder.com/50'" :alt="product.name">
                                </div>
                                <div class="product-info">
                                    <div class="product-name">{{ product.name }}</div>
                                    <div class="product-meta">
                                        <span class="product-price">฿{{ formatPrice(product.price) }}</span>
                                        <span class="product-sales">ขายแล้ว {{ product.sold }} ชิ้น</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Stock Alerts -->
                    <div class="grid-item stock-alerts">
                        <div class="section-header">
                            <h2>แจ้งเตือนสินค้าใกล้หมด</h2>
                            <button class="refresh-btn" @click="refreshStockAlerts"><i
                                    class="fas fa-sync-alt"></i></button>
                        </div>
                        <div class="alert-list">
                            <div v-for="product in lowStockProducts" :key="product.id" class="alert-item">
                                <div class="alert-icon" :class="{ 'critical': product.stock <= 5 }">
                                    <i class="fas fa-exclamation-triangle"></i>
                                </div>
                                <div class="alert-content">
                                    <div class="alert-title">{{ product.name }}</div>
                                    <div class="alert-message">เหลือในสต็อกเพียง <strong>{{ product.stock }}
                                            ชิ้น</strong></div>
                                </div>
                                <button class="alert-action" @click="navigateToProduct(product.id)">
                                    <i class="fas fa-external-link-alt"></i>
                                </button>
                            </div>
                            <div v-if="lowStockProducts.length === 0" class="empty-state">
                                <i class="fas fa-check-circle"></i>
                                <p>ไม่มีสินค้าใกล้หมด</p>
                            </div>
                        </div>
                    </div>

                    <!-- Recent Activities -->
                    <div class="grid-item recent-activities">
                        <div class="section-header">
                            <h2>กิจกรรมล่าสุด</h2>
                        </div>
                        <div class="timeline">
                            <div v-for="(activity, index) in recentActivities" :key="index" class="timeline-item">
                                <div class="timeline-icon" :class="activity.type">
                                    <i :class="getActivityIcon(activity.type)"></i>
                                </div>
                                <div class="timeline-content">
                                    <div class="timeline-time">{{ formatTime(activity.timestamp) }}</div>
                                    <div class="timeline-message">{{ activity.message }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Quick Actions Bar -->
                <div class="quick-actions">
                    <h3>คำสั่งด่วน</h3>
                    <div class="actions-container">
                        <div class="action-btn" @click="navigateTo('/admin/products', 'new')">
                            <i class="fas fa-plus"></i>
                            <span>เพิ่มสินค้าใหม่</span>
                        </div>
                        <div class="action-btn" @click="navigateTo('/admin/categories', 'new')">
                            <i class="fas fa-folder-plus"></i>
                            <span>เพิ่มหมวดหมู่</span>
                        </div>
                        <div class="action-btn" @click="navigateTo('/admin/users', 'new')">
                            <i class="fas fa-user-plus"></i>
                            <span>เพิ่มผู้ใช้</span>
                        </div>
                        <div class="action-btn" @click="navigateTo('/admin/orders')">
                            <i class="fas fa-shipping-fast"></i>
                            <span>จัดการออเดอร์</span>
                        </div>
                        <div class="action-btn" @click="navigateTo('/admin/reviews')">
                            <i class="fas fa-comments"></i>
                            <span>ตรวจสอบรีวิว</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script>
import AdminLayout from '~/components/admin/AdminLayout.vue';
import axios from 'axios';
// If using a chart library like Chart.js, you'd import it here:
// import Chart from 'chart.js/auto';

export default {
    components: {
        AdminLayout
    },
    data() {
        return {
            loading: true,
            error: null,
            dateRange: '30days', // 7days, 30days, year
            chartType: 'revenue', // revenue, orders
            totalRevenue: 0,
            revenueChange: 0,
            totalOrders: 0,
            orderChange: 0,
            newUsers: 0,
            userChange: 0,
            averageRating: 0,
            recentOrders: [],
            topProducts: [],
            lowStockProducts: [],
            recentActivities: [],
            chartInstance: null,
            categoriesCount: 0
        };
    },
    mounted() {
        this.fetchDashboardData();
    },
    watch: {
        dateRange() {
            this.fetchDashboardData();
        },
        chartType() {
            this.updateChart();
        }
    },
    methods: {
        async fetchDashboardData() {
            this.loading = true;

            try {
                // Fetch users data for the dashboard
                const usersResponse = await axios.get('http://localhost:8000/users/');
                this.newUsers = usersResponse.data.length;

                // Fetch categories count
                const categoriesResponse = await axios.get('http://localhost:8000/categories/');
                this.categoriesCount = categoriesResponse.data.length;

                // Fetch products data
                try {
                    const productsResponse = await axios.get('http://localhost:8000/products/');
                    const products = productsResponse.data;

                    // Calculate low stock products
                    this.lowStockProducts = products
                        .filter(product => product.stock < 10)
                        .sort((a, b) => a.stock - b.stock)
                        .slice(0, 5)
                        .map(product => ({
                            id: product.id,
                            name: product.name,
                            stock: product.stock
                        }));

                    // In a real app, you would also calculate top products
                    // based on actual sales data
                } catch (err) {
                    console.error('Error fetching products:', err);
                }

                this.loading = false;
            } catch (error) {
                this.error = 'Failed to load dashboard data';
                this.loading = false;
            }
        },
        formatPrice(price) {
            return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        },
        formatDate(dateString) {
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('th-TH', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            }).format(date);
        },
        formatTime(dateString) {
            const date = new Date(dateString);
            const now = new Date();
            const diffTime = Math.abs(now - date);
            const diffHours = Math.floor(diffTime / (1000 * 60 * 60));

            if (diffHours < 1) {
                const diffMinutes = Math.floor(diffTime / (1000 * 60));
                return `${diffMinutes} นาทีที่แล้ว`;
            } else if (diffHours < 24) {
                return `${diffHours} ชั่วโมงที่แล้ว`;
            } else {
                return this.formatDate(dateString);
            }
        },
        getStatusText(status) {
            const statusMap = {
                'pending': 'รอดำเนินการ',
                'processing': 'กำลังจัดส่ง',
                'delivered': 'จัดส่งแล้ว',
                'cancelled': 'ยกเลิก'
            };
            return statusMap[status] || status;
        },
        getActivityIcon(type) {
            const iconMap = {
                'order': 'fas fa-shopping-bag',
                'payment': 'fas fa-credit-card',
                'review': 'fas fa-star',
                'stock': 'fas fa-box',
                'user': 'fas fa-user'
            };
            return iconMap[type] || 'fas fa-bell';
        },
        navigateToOrder(id) {
            // In a real app this would navigate to the order detail page
            console.log('Navigate to order:', id);
        },
        navigateToProduct(id) {
            // In a real app this would navigate to the product edit page
            console.log('Navigate to product:', id);
        },
        navigateTo(path, action) {
            // In a real app this would navigate and possibly trigger an action
            console.log('Navigate to:', path, action);
        },
        refreshStockAlerts() {
            // In a real app this would refresh the stock alerts data
            console.log('Refreshing stock alerts');
        },
        initChart() {
            // This is a placeholder for chart initialization
            // In a real app, you would use a charting library like Chart.js
            console.log('Chart initialized');

            // Example of Chart.js implementation:
            /*
            if (typeof window !== 'undefined' && this.$refs.salesChart) {
              const ctx = this.$refs.salesChart.getContext('2d');
              this.chartInstance = new Chart(ctx, {
                type: 'line',
                data: this.getChartData(),
                options: {
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true
                    }
                  }
                }
              });
            }
            */
        },
        updateChart() {
            // This would update the chart data based on selected filters
            console.log('Updating chart with:', this.dateRange, this.chartType);

            // Example of Chart.js implementation:
            /*
            if (this.chartInstance) {
              this.chartInstance.data = this.getChartData();
              this.chartInstance.update();
            }
            */
        },
        getChartData() {
            // This would return the appropriate data based on selections
            // Mock data example:
            return {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [
                    {
                        label: this.chartType === 'revenue' ? 'ยอดขาย' : 'จำนวนคำสั่งซื้อ',
                        data: this.chartType === 'revenue'
                            ? [12000, 19000, 15000, 25000, 22000, 30000]
                            : [15, 25, 20, 30, 28, 35],
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.5)',
                        tension: 0.1
                    }
                ]
            };
        }
    }
};
</script>

<style scoped>
.dashboard-container
{
    padding: 20px;
    width: 100%;
    box-sizing: border-box;
}

.page-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.date-selector
{
    display: flex;
    gap: 10px;
}

.date-button
{
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
}

.date-button.active,
.date-button:hover
{
    background-color: #3498db;
    color: white;
    border-color: #3498db;
}

/* Stats Cards */
.stats-cards
{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
}

.stat-card
{
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.stat-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.stat-header h3
{
    margin: 0;
    font-size: 16px;
    color: #555;
}

.stat-icon
{
    font-size: 24px;
    padding: 10px;
    border-radius: 50%;
}

.stat-icon.revenue
{
    background-color: rgba(46, 204, 113, 0.1);
    color: #2ecc71;
}

.stat-icon.orders
{
    background-color: rgba(52, 152, 219, 0.1);
    color: #3498db;
}

.stat-icon.users
{
    background-color: rgba(155, 89, 182, 0.1);
    color: #9b59b6;
}

.stat-icon.reviews
{
    background-color: rgba(241, 196, 15, 0.1);
    color: #f1c40f;
}

.stat-value
{
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 10px;
}

.stat-change
{
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.stat-change.positive
{
    color: #2ecc71;
}

.stat-change.negative
{
    color: #e74c3c;
}

.rating-stars
{
    color: #ddd;
}

.rating-stars .filled
{
    color: #f1c40f;
}

/* Chart Section */
.chart-section
{
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.section-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}

.section-header h2
{
    margin: 0;
    font-size: 18px;
}

.section-actions select
{
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.chart-container
{
    height: 300px;
    position: relative;
}

/* Dashboard Grid */
.dashboard-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 24px;
}

.grid-item
{
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

/* Recent Orders */
.view-all
{
    color: #3498db;
    text-decoration: none;
    font-size: 14px;
}

.view-all:hover
{
    text-decoration: underline;
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
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

.data-table th
{
    color: #777;
    font-weight: 600;
}

.clickable
{
    cursor: pointer;
}

.clickable:hover
{
    background-color: #f9f9f9;
}

.status-badge
{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 500;
}

.status-badge.pending
{
    background-color: #fff8e1;
    color: #f57f17;
}

.status-badge.processing
{
    background-color: #e3f2fd;
    color: #1976d2;
}

.status-badge.delivered
{
    background-color: #e8f5e9;
    color: #2e7d32;
}

.status-badge.cancelled
{
    background-color: #ffebee;
    color: #c62828;
}

/* Top Products */
.product-list
{
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.product-item
{
    display: flex;
    align-items: center;
    gap: 15px;
}

.product-image
{
    width: 50px;
    height: 50px;
    border-radius: 8px;
    overflow: hidden;
}

.product-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.product-info
{
    flex: 1;
}

.product-name
{
    font-weight: 600;
    margin-bottom: 5px;
}

.product-meta
{
    display: flex;
    justify-content: space-between;
    font-size: 14px;
}

.product-price
{
    color: #e74c3c;
    font-weight: 500;
}

.product-sales
{
    color: #777;
}

/* Stock Alerts */
.refresh-btn
{
    background: none;
    border: none;
    color: #3498db;
    cursor: pointer;
    font-size: 16px;
}

.alert-list
{
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.alert-item
{
    display: flex;
    align-items: center;
    padding: 10px;
    border-radius: 8px;
    background-color: #f9f9f9;
    gap: 15px;
}

.alert-icon
{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #fff8e1;
    color: #f57f17;
}

.alert-icon.critical
{
    background-color: #ffebee;
    color: #c62828;
}

.alert-content
{
    flex: 1;
}

.alert-title
{
    font-weight: 600;
    margin-bottom: 5px;
}

.alert-message
{
    font-size: 14px;
    color: #777;
}

.alert-action
{
    background: none;
    border: none;
    color: #3498db;
    cursor: pointer;
    font-size: 16px;
}

.empty-state
{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 30px 0;
    color: #2ecc71;
    text-align: center;
}

.empty-state i
{
    font-size: 32px;
    margin-bottom: 10px;
}

.empty-state p
{
    margin: 0;
    color: #555;
}

/* Recent Activities */
.timeline
{
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.timeline-item
{
    display: flex;
    gap: 15px;
}

.timeline-icon
{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    flex-shrink: 0;
}

.timeline-icon.order
{
    background-color: rgba(52, 152, 219, 0.1);
    color: #3498db;
}

.timeline-icon.payment
{
    background-color: rgba(46, 204, 113, 0.1);
    color: #2ecc71;
}

.timeline-icon.review
{
    background-color: rgba(241, 196, 15, 0.1);
    color: #f1c40f;
}

.timeline-icon.stock
{
    background-color: rgba(231, 76, 60, 0.1);
    color: #e74c3c;
}

.timeline-icon.user
{
    background-color: rgba(155, 89, 182, 0.1);
    color: #9b59b6;
}

.timeline-content
{
    flex: 1;
}

.timeline-time
{
    font-size: 12px;
    color: #777;
    margin-bottom: 4px;
}

.timeline-message
{
    font-size: 14px;
}

/* Quick Actions Bar */
.quick-actions
{
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 24px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.quick-actions h3
{
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    color: #555;
}

.actions-container
{
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
}

.action-btn
{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 120px;
    height: 100px;
    background-color: #f5f7fa;
    border-radius: 8px;
    padding: 15px;
    cursor: pointer;
    transition: all 0.2s;
}

.action-btn:hover
{
    background-color: #e3f2fd;
    transform: translateY(-5px);
}

.action-btn i
{
    font-size: 24px;
    margin-bottom: 10px;
    color: #3498db;
}

.action-btn span
{
    text-align: center;
    font-size: 14px;
    color: #555;
}

/* Loading Container */
.loading-container
{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 400px;
}

.loading-spinner
{
    width: 50px;
    height: 50px;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
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

/* Media Queries */
@media (max-width: 992px)
{
    .dashboard-grid
    {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px)
{
    .stats-cards
    {
        grid-template-columns: 1fr 1fr;
    }

    .actions-container
    {
        justify-content: center;
    }
}

@media (max-width: 576px)
{
    .stats-cards
    {
        grid-template-columns: 1fr;
    }

    .date-selector
    {
        display: none;
    }

    .stat-header h3
    {
        font-size: 14px;
    }

    .stat-value
    {
        font-size: 24px;
    }
}
</style>