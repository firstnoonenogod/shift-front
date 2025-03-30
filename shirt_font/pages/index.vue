<template lang="html">
    <div class="container">
        <header class="header">
            <div class="logo" @click="$router.push('/')">CPE jersey shop</div>
            <div class="search-bar">
                <input type="text" v-model="searchQuery" placeholder="ค้นหาเสื้อผ้า..." @input="searchProducts"
                    @keyup.enter="searchProducts" />
                <button class="search-button" @click="searchProducts">ค้นหา</button>
            </div>
            <div class="nav-icons">
                <span class="icon" @click="$router.push('/cart')" title="ตะกร้าสินค้า">🛒</span>
                <span class="icon" @click="userMenu = !userMenu" title="บัญชีของฉัน">👤</span>
                <!-- User dropdown menu -->
                <div class="user-dropdown" v-if="userMenu" v-click-outside="closeUserMenu">
                    <div v-if="isLoggedIn">
                        <div class="user-info">
                            <div class="user-avatar">{{ userInitial }}</div>
                            <div class="user-name">{{ user.email }}</div>
                        </div>
                        <ul>
                            <li @click="$router.push('/profile'); userMenu = false">บัญชีของฉัน</li>
                            <li @click="$router.push('/profile?tab=orders'); userMenu = false">คำสั่งซื้อของฉัน</li>
                            <li @click="$router.push('/profile?tab=favorites'); userMenu = false">รายการโปรด</li>
                            <li @click="logout">ออกจากระบบ</li>
                        </ul>
                    </div>
                    <div v-else>
                        <ul>
                            <li @click="$router.push('/login'); userMenu = false">เข้าสู่ระบบ</li>
                            <li @click="$router.push('/register'); userMenu = false">สมัครสมาชิก</li>
                        </ul>
                    </div>
                </div>
            </div>
        </header>

        <section class="category-section">
            <h2>football jersey</h2>
            <div class="category-list">
                <div class="category-item" :class="{ active: selectedCategory === 'all' }"
                    @click="filterByCategory('all')">
                    ทั้งหมด
                </div>
                <div class="category-item" v-for="category in categories" :key="category.id"
                    :class="{ active: selectedCategory === category.id }" @click="filterByCategory(category.id)">
                    {{ category.name }}
                </div>
            </div>
        </section>

        <section class="product-section">
            <h2>{{ isSearchActive ? 'ผลการค้นหา: ' + searchQuery : categoryTitle }}</h2>
            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดสินค้า...</p>
            </div>
            <div v-else-if="displayedProducts.length === 0" class="no-products">
                <p>{{ isSearchActive ? 'ไม่พบสินค้าที่ตรงกับคำค้นหา' : 'ไม่พบสินค้าในหมวดหมู่นี้' }}</p>
            </div>
            <div v-else class="product-grid">
                <ProductCard v-for="product in displayedProducts" :key="product.id" :product="product" />
            </div>
        </section>

        <footer class="footer">
            <div class="footer-section">
                <h3>ช่วยเหลือ</h3>
                <ul>
                    <li>วิธีการสั่งซื้อ</li>
                    <li>การจัดส่ง</li>
                    <li>การชำระเงิน</li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>เกี่ยวกับเรา</h3>
                <ul>
                    <li>ข้อมูลบริษัท</li>
                    <li>ติดต่อเรา</li>
                </ul>
            </div>
        </footer>
    </div>
</template>

<script lang="ts">
import ProductCard from '~/components/ProductCard.vue';
import axios from 'axios';

export default {
    components: {
        ProductCard
    },
    data ()
    {
        return {
            searchQuery: '',
            userMenu: false,
            isLoggedIn: false,
            user: {
                email: 'user@example.com',
                id: ''
            },
            products: [],
            filteredProducts: [], // Renamed for clarity
            orders: [],
            selectedCategory: 'all',
            categories: [],
            loading: true,
            error: null,
            categoryMappings: {
                '67c15c52d19febc2739a72fa': 'Premier League',
                '67c15c74d19febc2739a72fb': 'Serie A',
                '67c15c9cd19febc2739a72fc': 'Bundesliga',
                '67c15cb1d19febc2739a72fd': 'LaLiga',
                '67c15cb9d19febc2739a72fe': 'Other',
                'all': 'ทั้งหมด'
            },
            isSearchActive: false // Added to track when search is active
        };
    },
    computed: {
        displayedProducts ()
        {
            if (!this.products || this.products.length === 0)
            {
                return [];
            }

            // If search is active, use the filtered results
            if (this.isSearchActive)
            {
                return this.filteredProducts;
            }

            // Otherwise filter by category
            if (this.selectedCategory === 'all')
            {
                return this.products;
            }

            return this.products.filter(product =>
                product && product.category_id === this.selectedCategory
            );
        },
        categoryTitle ()
        {
            return this.selectedCategory === 'all' ?
                'สินค้าทั้งหมด' :
                `${this.categoryMappings[this.selectedCategory] || 'สินค้า'}`;
        },
        userInitial ()
        {
            return this.user && this.user.email ? this.user.email.charAt(0).toUpperCase() : '';
        }
    },
    methods: {
        async fetchProducts ()
        {
            this.loading = true;
            this.error = null;

            try
            {
                const response = await axios.get('http://127.0.0.1:8000/products/');

                if (response && response.data)
                {
                    // Ensure each product has the required properties
                    this.products = response.data.map(product =>
                    {
                        // Make sure images is always an array
                        if (!product.images)
                        {
                            product.images = [];
                        } else if (!Array.isArray(product.images))
                        {
                            product.images = [product.images];
                        }

                        return product;
                    });

                    console.log('Products loaded:', this.products.length);
                } else
                {
                    this.products = [];
                    console.warn('No products data received');
                }
            } catch (error)
            {
                console.error('Error fetching products:', error);
                this.error = 'ไม่สามารถโหลดข้อมูลสินค้าได้';
                this.products = [];
            } finally
            {
                this.loading = false;
            }
        },
        async fetchCategories ()
        {
            try
            {
                const response = await axios.get('http://127.0.0.1:8000/categories/');
                if (response && response.data)
                {
                    this.categories = response.data;
                    console.log('Categories loaded:', this.categories.length);
                } else
                {
                    this.categories = [];
                    console.warn('No categories data received');
                }
            } catch (error)
            {
                console.error('Error fetching categories:', error);
                this.categories = [];
            }
        },
        filterByCategory (categoryId)
        {
            if (categoryId)
            {
                this.selectedCategory = categoryId;
            }
            // Clear any active searches
            this.searchQuery = '';
            this.filteredProducts = [];
            this.isSearchActive = false;
            console.log('Filtering by category:', categoryId);
        },
        async fetchOrders ()
        {
            try
            {
                // API logic for orders would go here
                console.log('Fetching orders...');
            } catch (error)
            {
                console.error('Error fetching orders:', error);
            }
        },
        searchProducts ()
        {
            const query = this.searchQuery.trim().toLowerCase();

            if (!query)
            {
                // Reset to category view if search is cleared
                this.isSearchActive = false;
                this.filteredProducts = [];
                console.log('Search cleared, showing category products');
                return;
            }

            console.log('Searching for products with query:', query);

            // Filter products based on search query
            this.filteredProducts = this.products.filter(product =>
            {
                if (!product) return false;

                const nameMatch = product.name && product.name.toLowerCase().includes(query);
                const descMatch = product.description && product.description.toLowerCase().includes(query);

                return nameMatch || descMatch;
            });

            // Set search as active
            this.isSearchActive = true;

            console.log(`Found ${this.filteredProducts.length} matching products`);
        },
        closeUserMenu ()
        {
            this.userMenu = false;
        },
        logout ()
        {
            // Implement logout logic here
            this.isLoggedIn = false;
            console.log('User logged out');
        }
    },
    async mounted ()
    {
        // Fetch categories first
        await this.fetchCategories();

        // Then fetch products
        await this.fetchProducts();

        // Fetch orders when component mounts
        await this.fetchOrders();
    }
};
</script>

<style lang="postcss">
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #f0f0f0;
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 100;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    color: #ee4d2d;
    cursor: pointer;
}

.search-bar {
    display: flex;
    width: 60%;
}

.search-bar input {
    flex-grow: 1;
    padding: 10px 15px;
    border: 2px solid #ee4d2d;
    border-right: none;
    border-radius: 2px 0 0 2px;
}

.search-button {
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 0 20px;
    cursor: pointer;
    border-radius: 0 2px 2px 0;
}

.nav-icons {
    display: flex;
    gap: 20px;
}

.icon {
    font-size: 20px;
    cursor: pointer;
}

.user-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    border: 1px solid #f0f0f0;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 200;
    width: 200px;
}

.user-info {
    display: flex;
    align-items: center;
    padding: 10px;
    border-bottom: 1px solid #f0f0f0;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #ee4d2d;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-right: 10px;
}

.user-name {
    font-size: 14px;
    color: #333;
}

.user-dropdown ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.user-dropdown li {
    padding: 10px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.user-dropdown li:hover {
    background-color: #f5f5f5;
}

.banner {
    margin: 20px 0;
    border-radius: 4px;
    overflow: hidden;
}

.banner img {
    width: 100%;
    height: auto;
}

.category-section {
    margin: 30px 0;
}

.category-list {
    display: flex;
    gap: 15px;
    overflow-x: auto;
    padding: 10px 0;
}

.category-item {
    min-width: 100px;
    text-align: center;
    padding: 10px;
    background-color: #f5f5f5;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.category-item:hover {
    background-color: rgba(238, 77, 45, 0.1);
    color: #ee4d2d;
}

.category-item.active {
    background-color: #ee4d2d;
    color: white;
}

.product-section {
    margin: 30px 0;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 20px;
}

.footer {
    display: flex;
    justify-content: space-between;
    padding: 40px 0;
    margin-top: 40px;
    border-top: 1px solid #f0f0f0;
}

.footer-section h3 {
    margin-bottom: 15px;
    font-size: 16px;
}

.footer-section ul {
    list-style: none;
    padding: 0;
}

.footer-section li {
    margin-bottom: 8px;
    color: #757575;
    cursor: pointer;
}

.footer-section li:hover {
    color: #ee4d2d;
}

h2 {
    color: #333;
    margin-bottom: 15px;
}

.loading-container {
    text-align: center;
    padding: 40px 0;
}

.loading-spinner {
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #ee4d2d;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.no-products {
    text-align: center;
    padding: 40px 0;
    color: #666;
}
</style>