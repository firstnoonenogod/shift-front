<template>
    <div class="container">
        <header class="header">
            <div class="logo" @click="$router.push('/')">ShirtShop</div>
            <div class="search-bar">
                <input type="text" placeholder="ค้นหาเสื้อผ้า..." />
                <button class="search-button">ค้นหา</button>
            </div>
            <div class="nav-icons">
                <span class="icon" @click="$router.push('/cart')">🛒</span>
                <span class="icon active">👤</span>
            </div>
        </header>

        <div class="profile-container">
            <div class="profile-sidebar">
                <div class="profile-avatar">
                    <div class="avatar">
                        {{ userInitials }}
                    </div>
                    <h3>{{ user.email }}</h3>
                </div>

                <div class="profile-menu">
                    <div class="menu-item active" @click="activeTab = 'profile'">
                        <span class="icon">👤</span>
                        <span>ข้อมูลส่วนตัว</span>
                    </div>
                    <div class="menu-item" @click="activeTab = 'orders'">
                        <span class="icon">📦</span>
                        <span>รายการสั่งซื้อ</span>
                    </div>
                    <div class="menu-item" @click="activeTab = 'reviews'">
                        <span class="icon">⭐</span>
                        <span>รีวิวของฉัน</span>
                    </div>
                    <div class="menu-item" @click="activeTab = 'favorites'">
                        <span class="icon">❤️</span>
                        <span>รายการโปรด</span>
                    </div>
                    <div class="menu-item" @click="activeTab = 'address'">
                        <span class="icon">🏠</span>
                        <span>ที่อยู่จัดส่ง</span>
                    </div>
                    <div class="menu-item logout" @click="logout">
                        <span class="icon">🚪</span>
                        <span>ออกจากระบบ</span>
                    </div>
                </div>
            </div>

            <div class="profile-content">
                <!-- Profile Section -->
                <div class="profile-section" v-if="activeTab === 'profile'">
                    <h2>ข้อมูลส่วนตัว</h2>

                    <div class="profile-form">
                        <div class="form-group">
                            <label>อีเมล</label>
                            <input type="email" v-model="user.email" disabled>
                            <span class="helper-text">ไม่สามารถแก้ไขได้</span>
                        </div>

                        <div class="form-group">
                            <label>เบอร์โทรศัพท์</label>
                            <input type="tel" v-model="user.phone">
                        </div>

                        <div class="form-group">
                            <label>ชื่อ-นามสกุล</label>
                            <input type="text" v-model="user.name" placeholder="กรุณากรอกชื่อ-นามสกุล">
                        </div>

                        <div class="form-row">
                            <div class="form-group half">
                                <label>วันเกิด</label>
                                <input type="date" v-model="user.birthdate">
                            </div>

                            <div class="form-group half">
                                <label>เพศ</label>
                                <select v-model="user.gender">
                                    <option value="">เลือกเพศ</option>
                                    <option value="male">ชาย</option>
                                    <option value="female">หญิง</option>
                                    <option value="other">อื่นๆ</option>
                                </select>
                            </div>
                        </div>

                        <button class="save-button" @click="saveProfile">บันทึกข้อมูล</button>
                    </div>
                </div>

                <!-- Orders Section -->
                <div class="orders-section" v-if="activeTab === 'orders'">
                    <h2>รายการสั่งซื้อ</h2>

                    <div class="order-tabs">
                        <div class="order-tab" :class="{ active: orderStatus === 'all' }" @click="orderStatus = 'all'">
                            ทั้งหมด</div>
                        <div class="order-tab" :class="{ active: orderStatus === 'pending' }"
                            @click="orderStatus = 'pending'">รอชำระเงิน</div>
                        <div class="order-tab" :class="{ active: orderStatus === 'processing' }"
                            @click="orderStatus = 'processing'">กำลังจัดส่ง</div>
                        <div class="order-tab" :class="{ active: orderStatus === 'completed' }"
                            @click="orderStatus = 'completed'">สำเร็จแล้ว</div>
                    </div>

                    <div class="order-list">
                        <div class="order-item" v-for="order in filteredOrders" :key="order.id">
                            <div class="order-header">
                                <div class="order-number">หมายเลขคำสั่งซื้อ: {{ order.id }}</div>
                                <div class="order-date">{{ order.date }}</div>
                                <div class="order-status" :class="order.status">{{ getStatusText(order.status) }}</div>
                            </div>

                            <div class="order-products">
                                <div class="order-product" v-for="product in order.products" :key="product.id">
                                    <img :src="product.image" :alt="product.name">
                                    <div class="product-details">
                                        <div class="product-name">{{ product.name }}</div>
                                        <div class="product-variant">{{ product.size }} / {{ product.color }}</div>
                                        <div class="product-price">฿{{ product.price }} x {{ product.quantity }}</div>
                                    </div>
                                </div>
                            </div>

                            <div class="order-footer">
                                <div class="order-total">
                                    <span>ยอดรวม:</span>
                                    <span class="price">฿{{ order.total }}</span>
                                </div>

                                <div class="order-actions">
                                    <button class="detail-button">ดูรายละเอียด</button>
                                    <button v-if="order.status === 'completed' && !order.reviewed"
                                        @click="showReviewModal(order)" class="review-button">
                                        รีวิวสินค้า
                                    </button>
                                </div>
                            </div>
                        </div>

                        <div class="empty-orders" v-if="filteredOrders.length === 0">
                            <div class="empty-icon">📦</div>
                            <div class="empty-text">ไม่พบรายการสั่งซื้อ</div>
                        </div>
                    </div>
                </div>

                <!-- Reviews Section -->
                <div class="reviews-section" v-if="activeTab === 'reviews'">
                    <h2>รีวิวของฉัน</h2>

                    <div class="review-list">
                        <div class="review-item" v-for="review in userReviews" :key="review.id">
                            <div class="review-product">
                                <img :src="review.product.image" :alt="review.product.name">
                                <div class="product-name">{{ review.product.name }}</div>
                            </div>

                            <div class="review-content">
                                <div class="review-rating">
                                    <div class="stars">
                                        <span v-for="i in 5" :key="i" :class="{ active: i <= review.rating }">★</span>
                                    </div>
                                    <div class="review-date">{{ review.date }}</div>
                                </div>

                                <div class="review-text">{{ review.comment }}</div>

                                <div class="review-images" v-if="review.images && review.images.length">
                                    <img v-for="(image, index) in review.images" :key="index" :src="image"
                                        :alt="'รีวิวรูปที่ ' + (index + 1)">
                                </div>
                            </div>
                        </div>

                        <div class="empty-reviews" v-if="userReviews.length === 0">
                            <div class="empty-icon">⭐</div>
                            <div class="empty-text">คุณยังไม่มีรีวิว</div>
                            <div class="empty-subtext">หลังจากซื้อสินค้าแล้วคุณจะสามารถรีวิวสินค้าที่นี่</div>
                        </div>
                    </div>
                </div>

                <!-- Address Section -->
                <div class="address-section" v-if="activeTab === 'address'">
                    <h2>ที่อยู่จัดส่ง</h2>

                    <div class="address-list" v-if="userAddresses.length > 0">
                        <div class="address-card" v-for="(address, index) in userAddresses" :key="index"
                            :class="{ 'default': address.isDefault }">
                            <div class="address-header">
                                <h3>{{ address.name }}</h3>
                                <div class="address-actions">
                                    <button class="edit-button" @click="editAddress(index)">แก้ไข</button>
                                    <button class="delete-button" @click="deleteAddress(index)"
                                        v-if="!address.isDefault">ลบ</button>
                                    <span class="default-badge" v-if="address.isDefault">ค่าเริ่มต้น</span>
                                    <button class="set-default-button" @click="setDefaultAddress(index)"
                                        v-if="!address.isDefault">
                                        ตั้งเป็นค่าเริ่มต้น
                                    </button>
                                </div>
                            </div>

                            <div class="address-info">
                                <p><strong>{{ address.recipientName }}</strong> | {{ address.phone }}</p>
                                <p>{{ address.addressDetail }}</p>
                                <p>{{ address.district }} {{ address.province }} {{ address.postalCode }}</p>
                            </div>
                        </div>

                        <button class="add-address-button" @click="showAddressForm = true; editingAddressIndex = null">
                            + เพิ่มที่อยู่ใหม่
                        </button>
                    </div>

                    <div class="empty-address" v-else>
                        <div class="empty-icon">🏠</div>
                        <div class="empty-text">คุณยังไม่มีที่อยู่จัดส่ง</div>
                        <button class="add-address-button" @click="showAddressForm = true">+ เพิ่มที่อยู่</button>
                    </div>
                </div>

                <!-- Favorites Section -->
                <div class="favorites-section" v-if="activeTab === 'favorites'">
                    <h2>รายการโปรด</h2>

                    <div class="product-grid" v-if="favoriteProducts.length > 0">
                        <div class="product-card" v-for="product in favoriteProducts" :key="product.id">
                            <div class="product-image">
                                <img :src="product.image" :alt="product.name">
                                <div class="discount-tag" v-if="product.discount">-{{ product.discount }}%</div>
                                <button class="remove-favorite" @click.stop="removeFromFavorites(product.id)">❌</button>
                            </div>
                            <div class="product-info" @click="goToProduct(product.id)">
                                <h3 class="product-name">{{ product.name }}</h3>
                                <div class="product-price">
                                    <span class="current-price">฿{{ product.price }}</span>
                                    <span class="original-price" v-if="product.originalPrice">฿{{ product.originalPrice
                                        }}</span>
                                </div>
                                <div class="product-meta">
                                    <div class="rating">
                                        <span class="stars">★</span>
                                        {{ product.rating }}
                                    </div>
                                    <div class="sold">ขายแล้ว {{ product.sold }} ชิ้น</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="empty-favorites" v-else>
                        <div class="empty-icon">❤️</div>
                        <div class="empty-text">ยังไม่มีรายการโปรด</div>
                        <div class="empty-subtext">คลิกที่ไอคอนหัวใจที่สินค้าเพื่อเพิ่มลงรายการโปรด</div>
                        <button class="browse-products-button" @click="$router.push('/')">เลือกซื้อสินค้า</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Review Modal -->
        <div class="modal-overlay" v-if="showReviewForm">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>รีวิวสินค้า</h2>
                    <button class="close-button" @click="showReviewForm = false">×</button>
                </div>

                <div class="modal-body">
                    <div class="review-products">
                        <div class="review-product" v-for="product in selectedOrder.products" :key="product.id">
                            <img :src="product.image" :alt="product.name">
                            <div class="product-name">{{ product.name }}</div>
                        </div>
                    </div>

                    <div class="rating-area">
                        <h3>ให้คะแนน</h3>
                        <div class="rating-stars">
                            <span v-for="i in 5" :key="i" :class="{ active: i <= reviewForm.rating }"
                                @click="reviewForm.rating = i">★</span>
                        </div>
                    </div>

                    <div class="form-group">
                        <label>ความคิดเห็น</label>
                        <textarea v-model="reviewForm.comment" placeholder="แชร์ประสบการณ์การใช้สินค้า"></textarea>
                    </div>

                    <div class="form-group">
                        <label>เพิ่มรูปภาพ (ไม่บังคับ)</label>
                        <div class="upload-area">
                            <div class="upload-preview" v-if="uploadedImages.length">
                                <div class="preview-image" v-for="(image, index) in uploadedImages" :key="index">
                                    <img :src="image">
                                    <button class="remove-image" @click="removeImage(index)">×</button>
                                </div>
                            </div>
                            <div class="upload-button" v-if="uploadedImages.length < 5">
                                <span>+ เพิ่มรูป</span>
                                <input type="file" accept="image/*" @change="handleImageUpload" multiple>
                            </div>
                            <div class="helper-text">อัปโหลดได้สูงสุด 5 รูป</div>
                        </div>
                    </div>

                    <button class="submit-review-button" @click="submitReview" :disabled="!canSubmitReview">
                        ส่งรีวิว
                    </button>
                </div>
            </div>
        </div>

        <!-- Address Form Modal -->
        <div class="modal-overlay" v-if="showAddressForm">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>{{ editingAddressIndex !== null ? 'แก้ไขที่อยู่' : 'เพิ่มที่อยู่ใหม่' }}</h2>
                    <button class="close-button" @click="showAddressForm = false">×</button>
                </div>

                <div class="modal-body">
                    <div class="form-group">
                        <label>ชื่อที่อยู่</label>
                        <input type="text" v-model="addressForm.name" placeholder="เช่น บ้าน, ที่ทำงาน">
                    </div>

                    <div class="form-group">
                        <label>ชื่อผู้รับ</label>
                        <input type="text" v-model="addressForm.recipientName" placeholder="กรุณากรอกชื่อผู้รับ">
                    </div>

                    <div class="form-group">
                        <label>เบอร์โทรศัพท์</label>
                        <input type="tel" v-model="addressForm.phone" placeholder="กรุณากรอกเบอร์โทรศัพท์">
                    </div>

                    <div class="form-group">
                        <label>ที่อยู่</label>
                        <textarea v-model="addressForm.addressDetail"
                            placeholder="บ้านเลขที่, หมู่บ้าน, ซอย, ถนน"></textarea>
                    </div>

                    <div class="form-row">
                        <div class="form-group half">
                            <label>แขวง/ตำบล</label>
                            <input type="text" v-model="addressForm.district" placeholder="แขวง/ตำบล">
                        </div>

                        <div class="form-group half">
                            <label>เขต/อำเภอ</label>
                            <input type="text" v-model="addressForm.amphoe" placeholder="เขต/อำเภอ">
                        </div>
                    </div>

                    <div class="form-row">
                        <div class="form-group half">
                            <label>จังหวัด</label>
                            <select v-model="addressForm.province">
                                <option value="">กรุณาเลือกจังหวัด</option>
                                <option v-for="province in provinces" :key="province" :value="province">
                                    {{ province }}
                                </option>
                            </select>
                        </div>

                        <div class="form-group half">
                            <label>รหัสไปรษณีย์</label>
                            <input type="text" v-model="addressForm.postalCode" placeholder="รหัสไปรษณีย์">
                        </div>
                    </div>

                    <div class="form-checkbox">
                        <input type="checkbox" id="defaultAddress" v-model="addressForm.isDefault">
                        <label for="defaultAddress">ตั้งเป็นที่อยู่หลัก</label>
                    </div>

                    <button class="save-address-button" @click="saveAddress">
                        {{ editingAddressIndex !== null ? 'บันทึกการแก้ไข' : 'บันทึกที่อยู่' }}
                    </button>
                </div>
            </div>
        </div>

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

<script>
export default {
    data() {
        return {
            user: {
                email: '',
                phone: '',
                name: '',
                birthdate: '',
                gender: '',
                address: ''
            },
            activeTab: 'profile',
            orderStatus: 'all',
            orders: [
                {
                    id: 'OD1234567890',
                    date: '25/06/2023',
                    status: 'completed',
                    reviewed: false,
                    total: 540,
                    products: [
                        {
                            id: 1,
                            name: 'เสื้อยืดคอกลมสีขาว',
                            size: 'M',
                            color: 'ขาว',
                            price: 250,
                            quantity: 2,
                            image: 'https://placeholder.pics/svg/80x80/DEDEDE/555555/T-SHIRT'
                        }
                    ]
                },
                {
                    id: 'OD0987654321',
                    date: '18/06/2023',
                    status: 'processing',
                    reviewed: false,
                    total: 390,
                    products: [
                        {
                            id: 2,
                            name: 'เสื้อยืดคอวีสีดำ',
                            size: 'L',
                            color: 'ดำ',
                            price: 290,
                            quantity: 1,
                            image: 'https://placeholder.pics/svg/80x80/DEDEDE/555555/T-SHIRT'
                        },
                        {
                            id: 3,
                            name: 'เสื้อโปโลสีกรมท่า',
                            size: 'M',
                            color: 'กรมท่า',
                            price: 450,
                            quantity: 1,
                            image: 'https://placeholder.pics/svg/80x80/DEDEDE/555555/POLO'
                        }
                    ]
                }
            ],
            userReviews: [
                {
                    id: 1,
                    productId: 4,
                    product: {
                        name: 'เสื้อเชิ้ตลายสก็อต',
                        image: 'https://placeholder.pics/svg/80x80/DEDEDE/555555/SHIRT'
                    },
                    rating: 5,
                    comment: 'สินค้าคุณภาพดีมาก ใส่สบาย ผ้านุ่ม ตัดเย็บประณีต สีสวยเหมือนในรูป ส่งเร็วมาก พอใจมากครับ แนะนำเลย',
                    date: '10/06/2023',
                    images: []
                }
            ],
            showReviewForm: false,
            selectedOrder: null,
            reviewForm: {
                rating: 5,
                comment: '',
            },
            uploadedImages: [],

            // Address section data
            userAddresses: [
                {
                    name: 'บ้าน',
                    recipientName: 'คุณทดสอบ นามสกุล',
                    phone: '0812345678',
                    addressDetail: '123/456 หมู่บ้านทดสอบ ซอย 5',
                    district: 'บางกะปิ',
                    amphoe: 'ห้วยขวาง',
                    province: 'กรุงเทพมหานคร',
                    postalCode: '10310',
                    isDefault: true
                }
            ],
            showAddressForm: false,
            editingAddressIndex: null,
            addressForm: {
                name: '',
                recipientName: '',
                phone: '',
                addressDetail: '',
                district: '',
                amphoe: '',
                province: '',
                postalCode: '',
                isDefault: false
            },
            provinces: [
                'กรุงเทพมหานคร', 'เชียงใหม่', 'ขอนแก่น', 'ชลบุรี', 'ภูเก็ต', 'สงขลา', 'นครราชสีมา',
                'อุดรธานี', 'เชียงราย', 'นครสวรรค์', 'สุราษฎร์ธานี', 'อุบลราชธานี', 'นนทบุรี'
            ],

            // Favorites section data
            favoriteProducts: [
                {
                    id: 3,
                    name: 'เสื้อโปโลสีกรมท่า',
                    price: 450,
                    originalPrice: 590,
                    discount: 24,
                    image: 'https://placeholder.pics/svg/200x200/DEDEDE/555555/POLO',
                    rating: 4.9,
                    sold: 650
                },
                {
                    id: 5,
                    name: 'เสื้อยืดลายกราฟิก',
                    price: 320,
                    originalPrice: 450,
                    discount: 29,
                    image: 'https://placeholder.pics/svg/200x200/DEDEDE/555555/GRAPHIC',
                    rating: 4.8,
                    sold: 1400
                }
            ]
        };
    },
    computed: {
        userInitials() {
            if (this.user.name) {
                return this.user.name.charAt(0).toUpperCase();
            } else if (this.user.email) {
                return this.user.email.charAt(0).toUpperCase();
            }
            return 'U';
        },
        filteredOrders() {
            if (this.orderStatus === 'all') {
                return this.orders;
            } else {
                return this.orders.filter(order => order.status === this.orderStatus);
            }
        },
        canSubmitReview() {
            return this.reviewForm.rating > 0 && this.reviewForm.comment.trim() !== '';
        }
    },
    created() {
        // Load user data from localStorage in a real app we'd fetch from API
        const storedUser = localStorage.getItem('user');
        if (storedUser) {
            const userData = JSON.parse(storedUser);
            this.user = { ...this.user, ...userData };
        }
    },
    methods: {
        getStatusText(status) {
            switch (status) {
                case 'pending': return 'รอชำระเงิน';
                case 'processing': return 'กำลังจัดส่ง';
                case 'completed': return 'สำเร็จแล้ว';
                case 'cancelled': return 'ยกเลิกแล้ว';
                default: return 'ไม่ระบุ';
            }
        },
        saveProfile() {
            // Save to localStorage for demo - in a real app we'd send to API
            localStorage.setItem('user', JSON.stringify(this.user));
            alert('บันทึกข้อมูลเรียบร้อยแล้ว');
        },
        showReviewModal(order) {
            this.selectedOrder = order;
            this.showReviewForm = true;
            this.reviewForm = {
                rating: 5,
                comment: ''
            };
            this.uploadedImages = [];
        },
        handleImageUpload(e) {
            if (this.uploadedImages.length >= 5) return;

            const files = Array.from(e.target.files);
            const remainingSlots = 5 - this.uploadedImages.length;
            const filesToProcess = files.slice(0, remainingSlots);

            filesToProcess.forEach(file => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.uploadedImages.push(e.target.result);
                };
                reader.readAsDataURL(file);
            });
        },
        removeImage(index) {
            this.uploadedImages.splice(index, 1);
        },
        submitReview() {
            if (!this.canSubmitReview) return;

            // In a real app, we'd send this to an API
            this.selectedOrder.reviewed = true;

            // Create a new review in the user's reviews
            this.userReviews.push({
                id: Date.now(),
                productId: this.selectedOrder.products[0].id,
                product: {
                    name: this.selectedOrder.products[0].name,
                    image: this.selectedOrder.products[0].image
                },
                rating: this.reviewForm.rating,
                comment: this.reviewForm.comment,
                date: new Date().toLocaleDateString('th-TH'),
                images: [...this.uploadedImages]
            });

            this.showReviewForm = false;
            alert('ส่งรีวิวเรียบร้อยแล้ว ขอบคุณสำหรับคำแนะนำ');
        },
        logout() {
            localStorage.removeItem('isLoggedIn');
            this.$router.push('/login');
        },
        // Address methods
        editAddress(index) {
            this.editingAddressIndex = index;
            this.addressForm = { ...this.userAddresses[index] };
            this.showAddressForm = true;
        },
        deleteAddress(index) {
            if (confirm('คุณแน่ใจหรือไม่ที่จะลบที่อยู่นี้?')) {
                this.userAddresses.splice(index, 1);
            }
        },
        setDefaultAddress(index) {
            this.userAddresses.forEach(addr => addr.isDefault = false);
            this.userAddresses[index].isDefault = true;
        },
        saveAddress() {
            if (this.addressForm.isDefault) {
                // Reset default status for all addresses
                this.userAddresses.forEach(addr => addr.isDefault = false);
            }

            if (this.editingAddressIndex !== null) {
                // Update existing address
                this.userAddresses[this.editingAddressIndex] = { ...this.addressForm };
            } else {
                // Add new address
                this.userAddresses.push({ ...this.addressForm });
            }

            this.showAddressForm = false;
            this.resetAddressForm();
        },
        resetAddressForm() {
            this.addressForm = {
                name: '',
                recipientName: '',
                phone: '',
                addressDetail: '',
                district: '',
                amphoe: '',
                province: '',
                postalCode: '',
                isDefault: false
            };
            this.editingAddressIndex = null;
        },

        // Favorites methods
        removeFromFavorites(id) {
            const index = this.favoriteProducts.findIndex(product => product.id === id);
            if (index > -1) {
                this.favoriteProducts.splice(index, 1);
            }
        },
        goToProduct(id) {
            this.$router.push(`/product/${id}`);
        }
    }
};
</script>

<style scoped>
.container
{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.header
{
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

.logo
{
    font-size: 24px;
    font-weight: bold;
    color: #ee4d2d;
    cursor: pointer;
}

.search-bar
{
    display: flex;
    width: 60%;
}

.search-bar input
{
    flex-grow: 1;
    padding: 10px 15px;
    border: 2px solid #ee4d2d;
    border-right: none;
    border-radius: 2px 0 0 2px;
}

.search-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 0 20px;
    cursor: pointer;
    border-radius: 0 2px 2px 0;
}

.nav-icons
{
    display: flex;
    gap: 20px;
}

.icon
{
    font-size: 20px;
    cursor: pointer;
}

.icon.active
{
    color: #ee4d2d;
}

.profile-container
{
    display: flex;
    gap: 30px;
    margin: 30px 0;
}

.profile-sidebar
{
    flex: 0 0 220px;
}

.profile-avatar
{
    background: white;
    border-radius: 8px;
    padding: 20px;
}

.profile-content
{
    flex: 1;
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Reviews styles */
.review-list
{
    margin-top: 20px;
}

.review-item
{
    display: flex;
    gap: 20px;
    padding: 20px;
    border-bottom: 1px solid #eee;
}

.review-product
{
    flex: 0 0 80px;
    text-align: center;
}

.review-product img
{
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    margin-bottom: 8px;
}

.review-product .product-name
{
    font-size: 12px;
    color: #666;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.review-content
{
    flex: 1;
}

.review-rating
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.stars
{
    color: #ccc;
    font-size: 18px;
}

.stars span.active
{
    color: #ff9500;
}

.review-date
{
    color: #999;
    font-size: 12px;
}

.review-text
{
    margin-bottom: 15px;
    line-height: 1.5;
}

.review-images
{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.review-images img
{
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
    cursor: pointer;
}

.empty-reviews,
.empty-favorites,
.empty-address,
.empty-orders
{
    text-align: center;
    padding: 40px 20px;
    color: #999;
}

.empty-icon
{
    font-size: 48px;
    margin-bottom: 15px;
}

.empty-text
{
    font-size: 18px;
    margin-bottom: 8px;
}

.empty-subtext
{
    margin-bottom: 20px;
}

/* Address styles */
.address-list
{
    margin-top: 20px;
}

.address-card
{
    border: 1px solid #eee;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
    position: relative;
    transition: all 0.3s;
}

.address-card.default
{
    border-color: #ee4d2d;
    background-color: rgba(238, 77, 45, 0.03);
}

.address-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.address-header h3
{
    margin: 0;
    color: #333;
}

.address-actions
{
    display: flex;
    gap: 10px;
    align-items: center;
}

.edit-button,
.delete-button,
.set-default-button
{
    background: none;
    border: none;
    font-size: 14px;
    cursor: pointer;
    padding: 0;
}

.edit-button,
.set-default-button
{
    color: #ee4d2d;
}

.delete-button
{
    color: #999;
}

.default-badge
{
    background-color: #ee4d2d;
    color: white;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 12px;
}

.address-info
{
    color: #666;
    line-height: 1.5;
}

.address-info p
{
    margin: 5px 0;
}

.add-address-button
{
    margin-top: 10px;
    background: none;
    border: 1px dashed #ccc;
    width: 100%;
    padding: 12px;
    border-radius: 4px;
    cursor: pointer;
    color: #ee4d2d;
    transition: all 0.3s;
}

.add-address-button:hover
{
    border-color: #ee4d2d;
    background-color: rgba(238, 77, 45, 0.03);
}

/* Form checkbox */
.form-checkbox
{
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.form-checkbox input
{
    margin-right: 10px;
    width: auto;
}

.save-address-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
}

/* Favorites styles */
.favorites-section .product-grid
{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.favorites-section .product-card
{
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.favorites-section .product-card:hover
{
    transform: translateY(-5px);
}

.favorites-section .product-image
{
    position: relative;
    height: 180px;
}

.favorites-section .product-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.remove-favorite
{
    position: absolute;
    top: 5px;
    right: 5px;
    background: rgba(255, 255, 255, 0.8);
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    font-size: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.browse-products-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
}

/* Review modal */
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
    background: white;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
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

.review-products
{
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.review-products .review-product
{
    flex-basis: calc(100% - 10px);
    display: flex;
    align-items: center;
    gap: 10px;
    text-align: left;
}

.review-products img
{
    width: 60px;
    height: 60px;
    border-radius: 4px;
    margin-bottom: 0;
}

.review-products .product-name
{
    font-size: 14px;
}

.rating-area
{
    margin-bottom: 20px;
}

.rating-area h3
{
    margin-bottom: 10px;
    color: #333;
}

.rating-stars
{
    font-size: 32px;
    color: #ccc;
    cursor: pointer;
}

.rating-stars span
{
    transition: color 0.2s;
    margin-right: 5px;
}

.rating-stars span.active,
.rating-stars span:hover
{
    color: #ff9500;
}

.upload-area
{
    border: 2px dashed #ddd;
    border-radius: 4px;
    padding: 20px;
    text-align: center;
    position: relative;
}

.upload-preview
{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}

.preview-image
{
    position: relative;
    width: 80px;
    height: 80px;
}

.preview-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
}

.remove-image
{
    position: absolute;
    top: -10px;
    right: -10px;
    background: rgba(0, 0, 0, 0.6);
    color: white;
    border: none;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    cursor: pointer;
}

.upload-button
{
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    color: #666;
    padding: 10px;
    border-radius: 4px;
    cursor: pointer;
    position: relative;
}

.upload-button input
{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

.helper-text
{
    color: #999;
    font-size: 12px;
    margin-top: 5px;
}

.submit-review-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 4px;
    cursor: pointer;
    width: 100%;
    font-weight: 600;
    margin-top: 10px;
}

.submit-review-button:disabled
{
    background-color: #ccc;
    cursor: not-allowed;
}
</style>