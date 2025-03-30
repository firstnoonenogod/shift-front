<template>
    <div class="product-page">
        <div class="container">
            <!-- Back Button -->
            <div class="back-navigation">
                <button @click="$router.back()" class="back-button">
                    <span class="back-icon">←</span> กลับ
                </button>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูลสินค้า...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <div class="error-icon">!</div>
                <h3>เกิดข้อผิดพลาด</h3>
                <p>{{ error }}</p>
                <button @click="fetchProductData" class="retry-button">ลองอีกครั้ง</button>
            </div>

            <div v-else class="product-container">
                <!-- Product Image Gallery -->
                <div class="product-gallery">
                    <div class="main-image-container">
                        <img :src="currentImage" :alt="product.name" class="main-image" />

                        <!-- Navigation arrows for images -->
                        <button v-if="product.images && product.images.length > 1" @click="prevImage"
                            class="gallery-nav prev" :disabled="currentImageIndex === 0">
                            ❮
                        </button>
                        <button v-if="product.images && product.images.length > 1" @click="nextImage"
                            class="gallery-nav next" :disabled="currentImageIndex >= product.images.length - 1">
                            ❯
                        </button>
                    </div>

                    <!-- Thumbnail images -->
                    <div v-if="product.images && product.images.length > 1" class="thumbnails">
                        <div v-for="(image, index) in product.images" :key="index" class="thumbnail"
                            :class="{ active: currentImageIndex === index }" @click="setCurrentImage(index)">
                            <img :src="image" :alt="`${product.name} - รูปที่ ${index + 1}`" />
                        </div>
                    </div>
                </div>

                <!-- Product Information -->
                <div class="product-info">
                    <h1 class="product-name">{{ product.name }}</h1>

                    <div class="product-meta">
                        <div class="product-id">รหัสสินค้า: {{ product.id }}</div>
                        <div class="product-stock">
                            สถานะ:
                            <span
                                :class="currentVariant ? (currentVariant.stock > 0 ? 'in-stock' : 'out-of-stock') : 'out-of-stock'">
                                {{ currentVariant ? (currentVariant.stock > 0 ? 'มีสินค้า' : 'สินค้าหมด') : 'กรุณาเลือกขนาด' }}
                            </span>
                        </div>
                    </div>

                    <div class="product-price">฿{{ currentVariant ? currentVariant.price : product.price }}</div>

                    <div class="product-variants" v-if="availableSizes.length > 0">
                        <h3>เลือกขนาด</h3>
                        <div class="size-options">
                            <button v-for="size in availableSizes" :key="size" class="size-btn"
                                :class="{ active: selectedSize === size, disabled: !isSizeInStock(size) }"
                                @click="selectSize(size)" :disabled="!isSizeInStock(size)">
                                {{ size }}
                            </button>
                        </div>
                    </div>

                    <div class="product-variants" v-if="availableColors.length > 0">
                        <h3>เลือกสี</h3>
                        <div class="color-options">
                            <button v-for="color in availableColors" :key="color" class="color-btn"
                                :class="{ active: selectedColor === color, disabled: !isColorAvailableForSize() }"
                                @click="selectColor(color)" :disabled="!isColorAvailableForSize()">
                                {{ color }}
                            </button>
                        </div>
                    </div>

                    <div class="quantity-selector">
                        <h3>จำนวน</h3>
                        <div class="quantity-control">
                            <button @click="decreaseQuantity" :disabled="quantity <= 1 || !currentVariant">-</button>
                            <input type="number" v-model.number="quantity" min="1"
                                :max="currentVariant ? currentVariant.stock : 0" @change="validateQuantity" />
                            <button @click="increaseQuantity"
                                :disabled="!currentVariant || quantity >= currentVariant.stock">+</button>
                        </div>
                        <span class="stock-info" v-if="currentVariant">
                            มีสินค้าเหลือ {{ currentVariant.stock }} ชิ้น
                        </span>
                        <span class="stock-info" v-else>
                            กรุณาเลือกขนาดเพื่อดูสินค้าคงเหลือ
                        </span>
                    </div>

                    <div class="product-actions">
                        <button @click="addToCart" class="add-to-cart-btn"
                            :disabled="!currentVariant || currentVariant.stock <= 0">
                            <span class="cart-icon">🛒</span> เพิ่มลงตะกร้า
                        </button>
                        <button @click="buyNow" class="buy-now-btn"
                            :disabled="!currentVariant || currentVariant.stock <= 0">ซื้อเลย</button>
                    </div>

                    <div class="product-guarantee">
                        <div class="guarantee-item">
                            <span class="guarantee-icon">✓</span>
                            <span>รับประกันสินค้าของแท้ 100%</span>
                        </div>
                        <div class="guarantee-item">
                            <span class="guarantee-icon">✓</span>
                            <span>จัดส่งฟรีเมื่อซื้อครบ ฿1,000</span>
                        </div>
                        <div class="guarantee-item">
                            <span class="guarantee-icon">✓</span>
                            <span>คืนสินค้าได้ภายใน 7 วัน</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Product Description Section -->
            <div v-if="!loading && !error" class="product-description-section">
                <div class="section-tabs">
                    <div class="tab" :class="{ active: activeTab === 'description' }"
                        @click="activeTab = 'description'">
                        รายละเอียดสินค้า
                    </div>
                    <div class="tab" :class="{ active: activeTab === 'reviews' }" @click="activeTab = 'reviews'">
                        รีวิว
                        <span v-if="filteredReviews.length" class="review-count">{{ filteredReviews.length }}</span>
                    </div>
                    <div class="tab" :class="{ active: activeTab === 'delivery' }" @click="activeTab = 'delivery'">
                        การจัดส่ง
                    </div>
                </div>

                <div class="tab-content">
                    <!-- Description Tab -->
                    <div v-if="activeTab === 'description'" class="description-content">
                        <div class="description-text">
                            <h3>รายละเอียด</h3>
                            <p>{{ product.description || 'ไม่มีคำอธิบายเพิ่มเติม' }}</p>
                        </div>

                        <div class="product-specs">
                            <h3>ข้อมูลจำเพาะ</h3>
                            <table class="specs-table">
                                <tr>
                                    <td>ประเภท</td>
                                    <td>{{ getCategoryName(product.category_id) }}</td>
                                </tr>
                                <tr>
                                    <td>รหัสสินค้า</td>
                                    <td>{{ product.id }}</td>
                                </tr>
                                <tr v-if="currentVariant">
                                    <td>สินค้าคงเหลือ</td>
                                    <td>{{ currentVariant.stock }} ชิ้น</td>
                                </tr>
                            </table>
                        </div>
                    </div>

                    <!-- Reviews Tab -->
                    <div v-else-if="activeTab === 'reviews'" class="reviews-content">
                        <div class="reviews-summary">
                            <div class="average-rating">
                                <div class="rating-number">{{ averageRating.toFixed(1) }}</div>
                                <div class="rating-stars">
                                    <div class="stars-container">
                                        <div class="stars-filled" :style="{ width: ratingPercentage + '%' }">★★★★★</div>
                                        <div class="stars-empty">★★★★★</div>
                                    </div>
                                    <div class="rating-count">{{ filteredReviews.length }} รีวิว</div>
                                </div>
                            </div>
                            <div class="rating-distribution">
                                <div v-for="i in 5" :key="i" class="rating-bar-container">
                                    <div class="rating-label">{{ 6 - i }} <span class="star">★</span></div>
                                    <div class="rating-bar-background">
                                        <div class="rating-bar-fill"
                                            :style="{ width: getRatingPercentage(6 - i) + '%' }"></div>
                                    </div>
                                    <div class="rating-count-small">{{ getRatingCount(6 - i) }}</div>
                                </div>
                            </div>
                        </div>

                        <div v-if="loadingReviews" class="loading-reviews">
                            <div class="loading-spinner-small"></div>
                            <p>กำลังโหลดรีวิว...</p>
                        </div>

                        <div v-else-if="filteredReviews.length === 0" class="no-reviews">
                            <div class="no-reviews-icon">💬</div>
                            <h3>ยังไม่มีรีวิวสำหรับสินค้านี้</h3>
                            <p>เป็นคนแรกที่รีวิวสินค้านี้และช่วยผู้ซื้อคนอื่น ๆ</p>
                        </div>

                        <div v-else class="reviews-list">
                            <div class="reviews-filter">
                                <span>กรองโดย:</span>
                                <button @click="activeFilter = 'all'" :class="{ active: activeFilter === 'all' }">
                                    ทั้งหมด ({{ filteredReviews.length }})
                                </button>
                                <button @click="activeFilter = 5" :class="{ active: activeFilter === 5 }">
                                    5 ดาว ({{ getRatingCount(5) }})
                                </button>
                                <button @click="activeFilter = 4" :class="{ active: activeFilter === 4 }">
                                    4 ดาว ({{ getRatingCount(4) }})
                                </button>
                                <button @click="activeFilter = 'comments'"
                                    :class="{ active: activeFilter === 'comments' }">
                                    มีข้อความ ({{ reviewsWithComments.length }})
                                </button>
                            </div>

                            <div v-for="(review, index) in displayedReviews" :key="index" class="review-item"
                                :class="{ 'with-comment': review.comment }">
                                <div class="review-header">
                                    <div class="reviewer-info">
                                        <div class="reviewer-avatar">{{ getRandomInitial() }}</div>
                                        <div class="reviewer-name">ลูกค้าที่ยืนยันแล้ว</div>
                                    </div>
                                    <div class="review-date">{{ getRandomDate() }}</div>
                                </div>
                                <div class="review-rating">
                                    <div class="review-stars">
                                        <span v-for="i in 5" :key="i" class="star"
                                            :class="{ filled: i <= review.rating }">★</span>
                                    </div>
                                    <div class="verified-purchase">✓ สั่งซื้อแล้ว</div>
                                </div>
                                <div v-if="review.comment" class="review-comment">
                                    {{ review.comment }}
                                </div>
                                <div class="review-footer">
                                    <div class="review-helpful">
                                        <button class="helpful-button" @click="markHelpful(index)">
                                            <span class="helpful-icon">👍</span>
                                            {{ review.helpful ? 'เป็นประโยชน์ (' + (review.helpfulCount || 1) + ')' : 'เป็นประโยชน์ (0)' }}
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div v-if="filteredReviews.length > reviewsPerPage" class="pagination">
                                <button @click="prevPage" :disabled="currentPage === 1">
                                    ก่อนหน้า
                                </button>
                                <div class="page-numbers">
                                    <span>หน้า {{ currentPage }} จาก {{ totalPages }}</span>
                                </div>
                                <button @click="nextPage" :disabled="currentPage === totalPages">
                                    ถัดไป
                                </button>
                            </div>
                        </div>

                        <div class="review-cta">
                            <h3>ซื้อสินค้านี้และเป็นคนแรกที่แสดงความคิดเห็น!</h3>
                            <p>แชร์ประสบการณ์การใช้งานของคุณกับลูกค้าคนอื่น ๆ</p>
                            <button class="buy-now-cta" @click="buyNow">ซื้อเลย</button>
                        </div>

                        <!-- Add ReviewForm Component at the bottom of the reviews tab -->
                        <ReviewForm :productId="product.id" @review-submitted="onReviewSubmitted"
                            @buy-product="buyNow" />
                    </div>

                    <!-- Delivery Tab -->
                    <div v-else-if="activeTab === 'delivery'" class="delivery-content">
                        <h3>ข้อมูลการจัดส่ง</h3>
                        <div class="shipping-options">
                            <div class="shipping-option">
                                <div class="shipping-icon">🚚</div>
                                <div class="shipping-details">
                                    <h4>จัดส่งแบบมาตรฐาน</h4>
                                    <p>ค่าจัดส่ง: ฿50</p>
                                    <p>ระยะเวลา: 3-5 วันทำการ</p>
                                </div>
                            </div>
                            <div class="shipping-option">
                                <div class="shipping-icon">🚀</div>
                                <div class="shipping-details">
                                    <h4>จัดส่งด่วน</h4>
                                    <p>ค่าจัดส่ง: ฿100</p>
                                    <p>ระยะเวลา: 1-2 วันทำการ</p>
                                </div>
                            </div>
                        </div>
                        <div class="shipping-note">
                            <p><strong>หมายเหตุ:</strong> สินค้าจะถูกจัดส่งภายใน 1 วันทำการหลังจากได้รับการชำระเงิน</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Cart Confirmation Modal -->
        <CartConfirmation :show="showCartConfirmation" :item="addedCartItem" @close="showCartConfirmation = false" />
    </div>
</template>

<script>
import axios from 'axios';
import CartConfirmation from '~/components/CartConfirmation.vue';
import ReviewForm from '~/components/product/ReviewForm.vue';

export default {
    components: {
        CartConfirmation,
        ReviewForm
    },
    data() {
        return {
            product: {},
            variants: [],
            loading: true,
            error: null,
            currentImageIndex: 0,
            quantity: 1,
            selectedSize: '',
            selectedColor: '',
            activeTab: 'description',
            loadingVariants: false,
            showCartConfirmation: false,
            addedCartItem: {},
            reviews: [],
            loadingReviews: false,
            activeFilter: 'all',
            currentPage: 1,
            reviewsPerPage: 20, // Updated to 20 per page
        };
    },
    computed: {
        currentImage() {
            if (this.product.images && this.product.images.length > 0) {
                return this.product.images[this.currentImageIndex];
            } else {
                return 'https://via.placeholder.com/500x500?text=No+Image';
            }
        },
        availableSizes() {
            if (!this.variants || this.variants.length === 0) return [];
            // Extract unique sizes from variants
            return [...new Set(this.variants.map(variant => variant.size))];
        },
        availableColors() {
            if (!this.variants || this.variants.length === 0) return [];
            // If a size is selected, only show colors for that size
            if (this.selectedSize) {
                const colorsBySize = this.variants
                    .filter(variant => variant.size === this.selectedSize)
                    .map(variant => variant.color);
                return [...new Set(colorsBySize)];
            }
            // Otherwise show all colors
            return [...new Set(this.variants.map(variant => variant.color))];
        },
        currentVariant() {
            if (!this.selectedSize) return null;

            // If both size and color are selected
            if (this.selectedSize && this.selectedColor) {
                return this.variants.find(v =>
                    v.size === this.selectedSize && v.color === this.selectedColor
                );
            }

            // If only size is selected, return the first variant with that size
            if (this.selectedSize) {
                return this.variants.find(v => v.size === this.selectedSize);
            }

            return null;
        },
        filteredReviews() {
            if (!this.reviews || this.reviews.length === 0) return [];

            // Filter reviews for current product
            const productReviews = this.reviews.filter(review => review.product_id === this.product.id);

            // Apply additional filters
            if (this.activeFilter === 'all') {
                return productReviews;
            } else if (this.activeFilter === 'comments') {
                return productReviews.filter(review => review.comment && review.comment.trim() !== '');
            } else {
                // Filter by star rating
                return productReviews.filter(review => review.rating === this.activeFilter);
            }
        },

        displayedReviews() {
            const startIndex = (this.currentPage - 1) * this.reviewsPerPage;
            return this.filteredReviews.slice(startIndex, startIndex + this.reviewsPerPage);
        },

        totalPages() {
            return Math.ceil(this.filteredReviews.length / this.reviewsPerPage);
        },

        averageRating() {
            if (!this.reviews || this.reviews.length === 0) return 0;

            const productReviews = this.reviews.filter(review => review.product_id === this.product.id);
            if (productReviews.length === 0) return 0;

            const totalRating = productReviews.reduce((sum, review) => sum + review.rating, 0);
            return totalRating / productReviews.length;
        },

        ratingPercentage() {
            return (this.averageRating / 5) * 100;
        },

        reviewsWithComments() {
            return this.reviews.filter(review =>
                review.product_id === this.product.id &&
                review.comment &&
                review.comment.trim() !== ''
            );
        }
    },
    async mounted() {
        await this.fetchProductData();
        this.fetchReviews();
    },
    methods: {
        async fetchProductData() {
            this.loading = true;
            this.error = null;
            const productId = this.$route.params.id;

            try {
                // Fetch product from API
                const response = await axios.get(`http://127.0.0.1:8000/products/${productId}`);
                this.product = response.data;

                // Handle empty images array case
                if (!this.product.images || !Array.isArray(this.product.images)) {
                    this.product.images = [];
                }

                console.log('Product loaded:', this.product);

                // Fetch product variants
                await this.fetchProductVariants(productId);

            } catch (error) {
                console.error('Error fetching product:', error);
                this.error = 'ไม่สามารถโหลดข้อมูลสินค้าได้ กรุณาลองใหม่อีกครั้ง';
            } finally {
                this.loading = false;
            }
        },

        async fetchProductVariants(productId) {
            this.loadingVariants = true;
            try {
                const response = await axios.get(`http://127.0.0.1:8000/variants/product/${productId}`);
                this.variants = response.data;
                console.log('Variants loaded:', this.variants);

                // Auto-select the first size if available
                if (this.availableSizes.length > 0) {
                    this.selectSize(this.availableSizes[0]);
                }
            } catch (error) {
                console.error('Error fetching variants:', error);
                this.error = 'ไม่สามารถโหลดข้อมูลตัวเลือกสินค้าได้';
            } finally {
                this.loadingVariants = false;
            }
        },

        async fetchReviews() {
            this.loadingReviews = true;
            const productId = this.$route.params.id;

            try {
                // Using the correct API endpoint with product_id filter and pagination
                const response = await axios.get(`http://localhost:8000/reviews/all`, {
                    params: {
                        product_id: productId,
                        skip: 0,
                        limit: 100 // Fetch more for client-side filtering
                    }
                });

                // Sort reviews by created_at date (newest first)
                this.reviews = Array.isArray(response.data)
                    ? response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                    : [];

                console.log('Reviews loaded:', this.reviews.length);
            } catch (error) {
                console.error('Error fetching reviews:', error);
                this.reviews = [];
            } finally {
                this.loadingReviews = false;
            }
        },

        getRatingCount(stars) {
            return this.reviews.filter(review =>
                review.product_id === this.product.id && review.rating === stars
            ).length;
        },

        getRatingPercentage(stars) {
            const count = this.getRatingCount(stars);
            const totalReviews = this.reviews.filter(review => review.product_id === this.product.id).length;
            return totalReviews > 0 ? (count / totalReviews) * 100 : 0;
        },

        getRandomInitial() {
            const initials = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T'];
            return initials[Math.floor(Math.random() * initials.length)];
        },

        getRandomDate() {
            const now = new Date();
            const daysAgo = Math.floor(Math.random() * 60) + 1; // Random between 1-60 days ago
            const date = new Date(now.getTime() - (daysAgo * 24 * 60 * 60 * 1000));

            return date.toLocaleDateString('th-TH', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            });
        },

        markHelpful(index) {
            const review = this.displayedReviews[index];
            if (!review.helpful) {
                review.helpful = true;
                review.helpfulCount = 1;
            } else {
                review.helpfulCount++;
            }
        },

        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },

        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },

        // Image Gallery Methods
        nextImage() {
            if (this.currentImageIndex < this.product.images.length - 1) {
                this.currentImageIndex++;
            }
        },
        prevImage() {
            if (this.currentImageIndex > 0) {
                this.currentImageIndex--;
            }
        },
        setCurrentImage(index) {
            this.currentImageIndex = index;
        },

        // Size and Color Selection
        selectSize(size) {
            this.selectedSize = size;

            // Reset color selection when size changes
            this.selectedColor = '';

            // Auto-select a color if there's only one available for this size
            const colorsForSize = [...new Set(this.variants
                .filter(v => v.size === size)
                .map(v => v.color))];

            if (colorsForSize.length === 1) {
                this.selectedColor = colorsForSize[0];
            }

            // Reset quantity if needed
            this.validateQuantity();
        },

        selectColor(color) {
            this.selectedColor = color;
            // Reset quantity if needed
            this.validateQuantity();
        },

        isSizeInStock(size) {
            // Check if there's any variant with this size that has stock
            return this.variants.some(v => v.size === size && v.stock > 0);
        },

        isColorAvailableForSize() {
            if (!this.selectedSize) return false;

            return this.variants.some(v =>
                v.size === this.selectedSize &&
                v.color === this.selectedColor &&
                v.stock > 0
            );
        },

        // Quantity Methods
        increaseQuantity() {
            if (this.currentVariant && this.quantity < this.currentVariant.stock) {
                this.quantity++;
            }
        },
        decreaseQuantity() {
            if (this.quantity > 1) {
                this.quantity--;
            }
        },
        validateQuantity() {
            if (!this.currentVariant) {
                this.quantity = 1;
                return;
            }

            if (this.quantity < 1 || isNaN(this.quantity)) {
                this.quantity = 1;
            } else if (this.quantity > this.currentVariant.stock) {
                this.quantity = this.currentVariant.stock;
            } else {
                this.quantity = Math.floor(this.quantity);
            }
        },

        // Cart Methods
        addToCart() {
            if (!this.currentVariant || this.currentVariant.stock <= 0) return;

            const item = {
                id: this.product.id,
                variant_id: this.currentVariant.product_id,
                name: this.product.name,
                price: this.currentVariant.price,
                quantity: this.quantity,
                size: this.selectedSize,
                color: this.selectedColor,
                image: this.currentImage,
                stock: this.currentVariant.stock
            };

            // Save to cart in localStorage
            const cart = JSON.parse(localStorage.getItem('cart') || '[]');
            cart.push(item);
            localStorage.setItem('cart', JSON.stringify(cart));

            // Store the added item for display in confirmation
            this.addedCartItem = item;

            return item;
        },

        buyNow() {
            if (!this.currentVariant || this.currentVariant.stock <= 0) return;

            // Add to cart and get the added item
            const item = this.addToCart();

            // Show confirmation
            if (item) {
                this.$router.push('/cart');
            }
        },

        onReviewSubmitted(review) {
            // Add the new review to our reviews collection
            this.reviews.unshift(review);

            // Reset filters to show all reviews
            this.activeFilter = 'all';
            this.currentPage = 1;

            // Show a success message
            alert('ขอบคุณสำหรับรีวิวของคุณ!');
        },

        // Helper Methods
        getCategoryName(categoryId) {
            const categories = {
                'premier-league': 'Premier League',
                'laliga': 'La Liga',
                'bundesliga': 'Bundesliga',
                'serie-a': 'Serie A',
                'jersey': 'Football Jersey',
                'football': 'Football Jersey',
                'shirt': 'Shirt'
            };

            return categories[categoryId] || categoryId || 'สินค้าทั่วไป';
        }
    },
    watch: {
        // Reload product data when the route param changes
        '$route.params.id': {
            handler(newId, oldId) {
                if (newId !== oldId) {
                    this.currentImageIndex = 0;
                    this.quantity = 1;
                    this.selectedSize = '';
                    this.selectedColor = '';
                    this.fetchProductData();
                }
            }
        }
    }
};
</script>

<style scoped>
.product-page
{
    padding: 30px 0 60px;
    background-color: #f8f8f8;
    min-height: calc(100vh - 60px);
}

.container
{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 15px;
}

/* Back Navigation */
.back-navigation
{
    padding: 0 0 20px;
}

.back-button
{
    background: none;
    border: none;
    font-size: 15px;
    color: #666;
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: color 0.2s;
}

.back-button:hover
{
    color: #ee4d2d;
}

.back-icon
{
    font-size: 18px;
    margin-right: 5px;
}

/* Loading and Error States */
.loading-container,
.error-container
{
    text-align: center;
    min-height: 400px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.loading-spinner
{
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #ee4d2d;
    border-radius: 50%;
    height: 50px;
    width: 50px;
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

.error-icon
{
    width: 60px;
    height: 60px;
    background-color: #ff4d4f;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
    margin-bottom: 20px;
}

.retry-button
{
    background-color: #ee4d2d;
    border: none;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    margin-top: 20px;
    transition: background-color 0.2s;
    cursor: pointer;
}

.retry-button:hover
{
    background-color: #d73211;
}

/* Product Container */
.product-container
{
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 40px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 30px;
}

/* Gallery Styling */
.product-gallery
{
    position: relative;
}

.main-image-container
{
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    height: 450px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #f8f8f8;
    margin-bottom: 15px;
}

.main-image
{
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

.gallery-nav
{
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255, 255, 255, 0.8);
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
    z-index: 2;
}

.gallery-nav:hover
{
    background: rgba(255, 255, 255, 0.95);
}

.gallery-nav.prev
{
    left: 15px;
}

.gallery-nav.next
{
    right: 15px;
}

.gallery-nav:disabled
{
    opacity: 0.4;
    cursor: not-allowed;
}

.thumbnails
{
    display: flex;
    gap: 10px;
    overflow-x: auto;
    padding-bottom: 10px;
}

.thumbnail
{
    height: 70px;
    width: 70px;
    border: 2px solid transparent;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    cursor: pointer;
}

.thumbnail.active
{
    border-color: #ee4d2d;
}

.thumbnail img
{
    height: 100%;
    width: 100%;
    object-fit: cover;
}

/* Product Information Styling */
.product-info
{
    display: flex;
    flex-direction: column;
}

.product-name
{
    font-size: 24px;
    margin-top: 0;
    margin-bottom: 15px;
    color: #333;
    line-height: 1.3;
}

.product-meta
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    color: #666;
    font-size: 14px;
}

.in-stock
{
    color: #52c41a;
    font-weight: bold;
}

.out-of-stock
{
    color: #ff4d4f;
    font-weight: bold;
}

.product-price
{
    color: #ee4d2d;
    font-weight: 600;
    margin-bottom: 25px;
}

.product-variants,
.quantity-selector
{
    margin-bottom: 25px;
}

.product-variants h3,
.quantity-selector h3
{
    font-size: 16px;
    margin-bottom: 10px;
    font-weight: 500;
    color: #333;
}

.size-options
{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.size-btn
{
    min-width: 50px;
    height: 35px;
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
}

.size-btn:hover
{
    border-color: #ee4d2d;
}

.size-btn.active
{
    border-color: #ee4d2d;
    color: #ee4d2d;
    font-weight: 600;
}

.quantity-selector
{
    margin-bottom: 30px;
}

.quantity-control
{
    display: flex;
    align-items: center;
    max-width: 120px;
}

.quantity-control button
{
    width: 35px;
    height: 35px;
    background: #f8f8f8;
    border: 1px solid #ddd;
    font-size: 16px;
    cursor: pointer;
    display: flex;
    justify-content: center;
    align-items: center;
}

.quantity-control button:first-child
{
    border-radius: 4px 0 0 4px;
}

.quantity-control button:last-child
{
    border-radius: 0 4px 4px 0;
}

.quantity-control input
{
    height: 35px;
    width: 50px;
    border: 1px solid #ddd;
    text-align: center;
    font-size: 14px;
    border-left: none;
    border-right: none;
}

.stock-info
{
    margin-top: 8px;
    font-size: 14px;
    color: #666;
}

.product-actions
{
    display: flex;
    gap: 15px;
    margin-bottom: 30px;
}

.add-to-cart-btn,
.buy-now-btn
{
    flex: 1;
    padding: 12px;
    font-size: 16px;
    cursor: pointer;
    border-radius: 4px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
}

.add-to-cart-btn
{
    background-color: white;
    border: 1px solid #ee4d2d;
    color: #ee4d2d;
}

.add-to-cart-btn:hover
{
    background-color: rgba(238, 77, 45, 0.05);
}

.buy-now-btn
{
    background-color: #ee4d2d;
    border: 1px solid #ee4d2d;
    color: white;
}

.buy-now-btn:hover
{
    background-color: #d73211;
}

.add-to-cart-btn:disabled,
.buy-now-btn:disabled
{
    background-color: #f5f5f5;
    border-color: #ddd;
    cursor: not-allowed;
    color: #aaa;
}

.cart-icon
{
    margin-right: 8px;
}

.product-guarantee
{
    border-top: 1px solid #f0f0f0;
    padding-top: 20px;
}

.guarantee-item
{
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    font-size: 14px;
    color: #666;
}

.guarantee-icon
{
    margin-right: 10px;
    color: #52c41a;
    font-weight: bold;
}

/* Description Section Styling */
.product-description-section
{
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 30px;
}

.section-tabs
{
    display: flex;
    border-bottom: 1px solid #f0f0f0;
    margin-bottom: 20px;
}

.tab
{
    padding: 15px 30px;
    font-weight: 600;
    cursor: pointer;
    transition: color 0.2s;
    position: relative;
}

.tab:not(.active):hover
{
    color: #ee4d2d;
}

.tab.active
{
    color: #ee4d2d;
}

.tab.active:after
{
    position: absolute;
    content: '';
    bottom: -1px;
    left: 0;
    height: 2px;
    width: 100%;
    background-color: #ee4d2d;
}

.description-text,
.product-specs
{
    margin-bottom: 30px;
}

.description-text h3,
.product-specs h3
{
    font-size: 18px;
    margin-bottom: 15px;
    color: #333;
}

.description-text p
{
    font-size: 15px;
    color: #666;
    line-height: 1.5;
    white-space: pre-wrap;
    margin: 0;
}

.specs-table
{
    border-collapse: collapse;
    width: 100%;
}

.specs-table tr
{
    border-bottom: 1px solid #f0f0f0;
}

.specs-table tr:last-child
{
    border-bottom: none;
}

.specs-table td
{
    padding: 12px 0;
    color: #666;
    font-size: 14px;
}

.specs-table td:first-child
{
    color: #333;
    font-weight: 500;
    width: 150px;
}

/* Delivery Tab Styling */
.delivery-content h3
{
    font-size: 18px;
    margin-bottom: 20px;
    color: #333;
}

.shipping-options
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    margin-bottom: 30px;
}

.shipping-option
{
    display: flex;
    padding: 15px;
    border: 1px solid #f0f0f0;
    border-radius: 8px;
}

.shipping-icon
{
    font-size: 24px;
    margin-right: 15px;
    color: #ee4d2d;
}

.shipping-details h4
{
    margin: 0 0 8px 0;
    color: #333;
}

.shipping-details p
{
    margin: 5px 0;
    font-size: 14px;
    color: #666;
}

.shipping-note
{
    background-color: #fafafa;
    padding: 15px;
    border-radius: 8px;
    color: #666;
    font-size: 14px;
    border-left: 3px solid #ee4d2d;
}

/* Responsive Styles */
@media (max-width: 992px)
{
    .product-container
    {
        grid-template-columns: 1fr;
        gap: 30px;
    }

    .main-image-container
    {
        height: 350px;
    }

    .shipping-options
    {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 576px)
{
    .product-actions
    {
        flex-direction: column;
    }

    .tab
    {
        padding: 15px;
    }
}

.size-btn.disabled
{
    cursor: not-allowed;
    opacity: 0.5;
    border-color: #ddd;
    color: #999;
}

.color-options
{
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.color-btn
{
    min-width: 50px;
    height: 35px;
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 14px;
}

.color-btn:hover:not(.disabled)
{
    border-color: #ee4d2d;
}

.color-btn.active
{
    border-color: #ee4d2d;
    color: #ee4d2d;
    font-weight: 600;
}

.color-btn.disabled
{
    cursor: not-allowed;
    opacity: 0.5;
    border-color: #ddd;
    color: #999;
}

/* Reviews Tab Styles */
.reviews-content
{
    padding: 20px 0;
}

.reviews-summary
{
    display: flex;
    gap: 40px;
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
}

.average-rating
{
    display: flex;
    align-items: center;
    gap: 15px;
}

.rating-number
{
    font-size: 48px;
    color: #ee4d2d;
    font-weight: 700;
    min-width: 80px;
    text-align: center;
}

.rating-stars
{
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.stars-container
{
    position: relative;
    font-size: 24px;
    display: inline-block;
}

.stars-empty
{
    color: #e0e0e0;
}

.stars-filled
{
    color: #ffb400;
    overflow: hidden;
    position: absolute;
    top: 0;
    left: 0;
    white-space: nowrap;
}

.rating-count
{
    font-size: 14px;
    color: #666;
}

.rating-distribution
{
    flex-grow: 1;
}

.rating-bar-container
{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
}

.rating-label
{
    display: flex;
    align-items: center;
    gap: 3px;
    min-width: 50px;
}

.rating-label .star
{
    color: #ffb400;
}

.rating-bar-background
{
    flex-grow: 1;
    background-color: #e0e0e0;
    height: 8px;
    border-radius: 4px;
    overflow: hidden;
}

.rating-bar-fill
{
    background-color: #ffb400;
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}

.rating-count-small
{
    text-align: right;
    min-width: 30px;
    color: #666;
    font-size: 14px;
}

.loading-reviews
{
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 30px 0;
}

.loading-spinner-small
{
    border: 3px solid rgba(0, 0, 0, 0.1);
    border-left-color: #ee4d2d;
    border-radius: 50%;
    height: 30px;
    width: 30px;
    animation: spin 1s linear infinite;
    margin-bottom: 15px;
}

.no-reviews
{
    text-align: center;
    padding: 40px 0;
}

.no-reviews-icon
{
    font-size: 36px;
    margin-bottom: 15px;
    color: #ccc;
}

.no-reviews h3
{
    color: #333;
    margin-bottom: 10px;
}

.no-reviews p
{
    color: #666;
}

.reviews-filter
{
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 15px;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 15px;
}

.reviews-filter span
{
    color: #666;
}

.reviews-filter button
{
    border: 1px solid #ddd;
    padding: 6px 12px;
    background-color: white;
    cursor: pointer;
    border-radius: 16px;
    font-size: 13px;
    transition: all 0.2s;
}

.reviews-filter button:hover
{
    border-color: #ee4d2d;
    color: #ee4d2d;
}

.reviews-filter button.active
{
    background-color: #ee4d2d;
    color: white;
    border-color: #ee4d2d;
}

.review-item.with-comment
{
    background-color: #fffef7;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review-header
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}

.reviewer-info
{
    display: flex;
    align-items: center;
}

.reviewer-avatar
{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #ee4d2d;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    margin-right: 10px;
}

.reviewer-name
{
    font-weight: 600;
    color: #333;
}

.review-date
{
    color: #999;
    font-size: 12px;
}

.review-rating
{
    display: flex;
    margin-bottom: 10px;
}

.review-stars
{
    display: flex;
    gap: 2px;
    margin-right: 15px;
}

.star
{
    color: #e0e0e0;
}

.star.filled
{
    color: #ffb400;
}

.verified-purchase
{
    font-size: 13px;
    color: #4CAF50;
    display: flex;
    align-items: center;
}

.review-comment
{
    margin-bottom: 15px;
    padding: 10px 0;
    line-height: 1.6;
}

.review-footer
{
    display: flex;
    justify-content: flex-end;
}

.helpful-button
{
    background: none;
    border: 1px solid #ddd;
    display: flex;
    align-items: center;
    padding: 6px 12px;
    border-radius: 4px;
    gap: 5px;
    cursor: pointer;
    font-size: 13px;
    color: #666;
}

.helpful-button:hover
{
    border-color: #ccc;
    background-color: #f9f9f9;
}

.pagination
{
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 30px 0;
}

.pagination button
{
    padding: 8px 15px;
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 4px;
    cursor: pointer;
}

.pagination button:disabled
{
    opacity: 0.5;
    cursor: not-allowed;
}

.page-numbers
{
    display: flex;
    align-items: center;
    padding: 0 15px;
    color: #666;
}

.review-cta
{
    margin-top: 40px;
    background-color: #f8f8ff;
    padding: 25px;
    border-radius: 8px;
    text-align: center;
    border: 1px solid #e6e6ff;
}

.review-cta h3
{
    color: #333;
    margin-bottom: 10px;
}

.review-cta p
{
    color: #666;
    margin-bottom: 20px;
}

.buy-now-cta
{
    background-color: #ee4d2d;
    color: white;
    padding: 12px 30px;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    font-weight: 600;
    transition: background-color 0.2s;
    cursor: pointer;
}

.buy-now-cta:hover
{
    background-color: #d73211;
}

.review-count
{
    background-color: #ee4d2d;
    color: white;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 12px;
    margin-left: 5px;
}

@media (max-width: 768px)
{
    .reviews-summary
    {
        flex-direction: column;
        gap: 20px;
    }

    .average-rating
    {
        justify-content: center;
    }

    .review-header
    {
        flex-direction: column;
        gap: 5px;
    }
}
</style>