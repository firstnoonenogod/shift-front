<template>
    <AdminLayout>
        <div class="reviews-management">
            <div class="page-header">
                <h1>จัดการรีวิว</h1>
            </div>

            <div class="filter-section">
                <div class="search-box">
                    <input type="text" v-model="searchQuery" placeholder="ค้นหารีวิว..." />
                </div>
                <div class="filter-box">
                    <select v-model="productFilter">
                        <option value="">ทุกสินค้า</option>
                        <option v-for="product in products" :key="product.id" :value="product.id">
                            {{ product.name }}
                        </option>
                    </select>
                    <select v-model="ratingFilter">
                        <option value="">ทุกคะแนน</option>
                        <option value="5">5 ดาว</option>
                        <option value="4">4 ดาว</option>
                        <option value="3">3 ดาว</option>
                        <option value="2">2 ดาว</option>
                        <option value="1">1 ดาว</option>
                    </select>
                    <select v-model="statusFilter">
                        <option value="">ทุกสถานะ</option>
                        <option value="approved">อนุมัติแล้ว</option>
                        <option value="pending">รอตรวจสอบ</option>
                        <option value="rejected">ไม่อนุมัติ</option>
                    </select>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <p>{{ error }}</p>
                <button @click="fetchReviews" class="retry-button">ลองใหม่</button>
            </div>

            <div v-else class="reviews-container">
                <div v-for="review in paginatedReviews" :key="review.id" class="review-card">
                    <div class="review-header">
                        <div class="user-info">
                            <div class="user-avatar">{{ getUserInitial(review.user_id) }}</div>
                            <div>
                                <div class="user-name">{{ getUserName(review.user_id) }}</div>
                                <div class="review-date">{{ formatDate(review.created_at) }}</div>
                            </div>
                        </div>
                        <div class="review-actions">
                            <div class="status-badge" :class="review.status || 'pending'">
                                {{ getStatusName(review.status || 'pending') }}
                            </div>
                            <div class="dropdown">
                                <button class="dropdown-toggle">
                                    <i class="fas fa-ellipsis-v"></i>
                                </button>
                                <div class="dropdown-menu">
                                    <button @click="approveReview(review)" v-if="review.status !== 'approved'">
                                        <i class="fas fa-check"></i> อนุมัติ
                                    </button>
                                    <button @click="rejectReview(review)" v-if="review.status !== 'rejected'">
                                        <i class="fas fa-ban"></i> ไม่อนุมัติ
                                    </button>
                                    <button @click="confirmDeleteReview(review)">
                                        <i class="fas fa-trash"></i> ลบรีวิว
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="review-product">
                        <div class="product-image">
                            <img :src="getProductImage(review.product_id)" :alt="getProductName(review.product_id)">
                        </div>
                        <div class="product-info">
                            <div class="product-name">{{ getProductName(review.product_id) }}</div>
                            <div class="rating">
                                <div class="stars">
                                    <i v-for="i in 5" :key="i" class="fas fa-star"
                                        :class="i <= review.rating ? 'filled' : ''"></i>
                                </div>
                                <span class="rating-value">{{ review.rating }}.0</span>
                            </div>
                        </div>
                    </div>

                    <div class="review-content">
                        <h3 class="review-title">{{ review.title }}</h3>
                        <p class="review-text">{{ review.content }}</p>
                    </div>

                    <div v-if="review.images && review.images.length > 0" class="review-images">
                        <img v-for="(image, index) in review.images" :key="index" :src="image"
                            @click="openImageModal(image)" class="review-image">
                    </div>
                </div>

                <div v-if="paginatedReviews.length === 0" class="empty-state">
                    <p>ไม่พบรีวิวที่ตรงกับเงื่อนไขการค้นหา</p>
                </div>

                <div class="pagination" v-if="totalPages > 1">
                    <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">&laquo; ก่อนหน้า</button>
                    <span>หน้า {{ currentPage }} จาก {{ totalPages }}</span>
                    <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">ถัดไป
                        &raquo;</button>
                </div>
            </div>
        </div>

        <!-- Edit Review Modal -->
        <div v-if="showEditModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>แก้ไขรีวิว</h2>
                    <button class="close-button" @click="closeModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label for="reviewRating">คะแนน</label>
                        <div class="rating-select">
                            <span v-for="i in 5" :key="i" class="star" :class="{ filled: i <= formData.rating }"
                                @click="formData.rating = i">★</span>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="reviewComment">ความคิดเห็น</label>
                        <textarea id="reviewComment" v-model="formData.comment" rows="4"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="reviewStatus">สถานะ</label>
                        <select id="reviewStatus" v-model="formData.status">
                            <option value="approved">อนุมัติ</option>
                            <option value="pending">รอการอนุมัติ</option>
                            <option value="rejected">ไม่อนุมัติ</option>
                        </select>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeModal">ยกเลิก</button>
                    <button class="save-button" @click="saveReview">บันทึก</button>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal">
                <div class="modal-header">
                    <h2>ยืนยันการลบรีวิว</h2>
                    <button class="close-button" @click="showDeleteModal = false">&times;</button>
                </div>
                <div class="modal-body">
                    <p>คุณต้องการลบรีวิวของสินค้า <strong>{{ getProductName(reviewToDelete.product_id) }}</strong>
                        ใช่หรือไม่?</p>
                    <p class="warning">การลบรายการนี้จะไม่สามารถกู้คืนได้</p>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="showDeleteModal = false">ยกเลิก</button>
                    <button class="delete-button" @click="deleteReview">ยืนยันการลบ</button>
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script>
import AdminLayout from '~/components/admin/AdminLayout.vue';
import axios from 'axios';
import { getProductPlaceholder } from '~/utils/imagePlaceholder';

export default {
    components: {
        AdminLayout
    },
    data() {
        return {
            reviews: [],
            products: [],
            users: {},
            loading: false,
            error: null,
            searchQuery: '',
            productFilter: '',
            ratingFilter: '',
            statusFilter: '',
            currentPage: 1,
            itemsPerPage: 50, // Updated to 50 per page
            showEditModal: false,
            showDeleteModal: false,
            formData: {
                rating: 5,
                comment: '',
                status: 'approved'
            },
            reviewToEdit: null,
            reviewToDelete: {},
            noImagePlaceholder: null
        };
    },
    computed: {
        filteredReviews() {
            // Ensure reviews is always an array
            if (!this.reviews || !Array.isArray(this.reviews)) {
                return [];
            }

            let result = [...this.reviews];

            // Apply search filter
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                result = result.filter(review =>
                    (review.comment && review.comment.toLowerCase().includes(query)) ||
                    (this.getUserName(review.user_id).toLowerCase().includes(query)) ||
                    (review.product_id && this.getProductName(review.product_id).toLowerCase().includes(query))
                );
            }

            // Apply product filter
            if (this.productFilter) {
                result = result.filter(review => review.product_id === this.productFilter);
            }

            // Apply rating filter
            if (this.ratingFilter) {
                const rating = parseInt(this.ratingFilter);
                result = result.filter(review => review.rating === rating);
            }

            // Apply status filter
            if (this.statusFilter) {
                result = result.filter(review => review.status === this.statusFilter);
            }

            return result;
        },

        paginatedReviews() {
            // Ensure filteredReviews is an array before using slice
            if (!Array.isArray(this.filteredReviews)) {
                return [];
            }

            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredReviews.slice(startIndex, startIndex + this.itemsPerPage);
        },

        totalPages() {
            if (!Array.isArray(this.filteredReviews)) {
                return 1;
            }
            return Math.max(1, Math.ceil(this.filteredReviews.length / this.itemsPerPage));
        }
    },
    mounted() {
        try {
            this.noImagePlaceholder = getProductPlaceholder(100, 100, 'No Image');
        } catch (e) {
            // Fallback for SSR where canvas might not be available
            this.noImagePlaceholder = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlMmUyZTIiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyNnB4IiBmaWxsPSIjOTk5OTk5Ij5ObyBJbWFnZTwvdGV4dD48L3N2Zz4=';
        }

        this.fetchProducts();
        this.fetchReviews();
    },
    methods: {
        async fetchProducts() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/products/');
                this.products = Array.isArray(response.data) ? response.data : [];
            } catch (err) {
                console.error('Error fetching products:', err);
                this.products = [];
                this.error = 'ไม่สามารถโหลดข้อมูลสินค้าได้';
            }
        },

        async fetchUser(userId) {
            // If we already have fetched this user, return
            if (this.users[userId]) return;

            try {
                const response = await axios.get(`http://127.0.0.1:8000/users/${userId}`);
                this.users[userId] = response.data;
            } catch (err) {
                console.error(`Error fetching user ${userId}:`, err);
                this.users[userId] = { name: 'ผู้ใช้ไม่ระบุชื่อ' };
            }
        },

        getUserName(userId) {
            if (!userId) return 'ผู้ใช้ไม่ระบุชื่อ';

            // If we have the user data, return the name
            if (this.users[userId]) {
                return this.users[userId].name || 'ผู้ใช้ไม่ระบุชื่อ';
            }

            // Otherwise fetch the user data and return a placeholder
            this.fetchUser(userId);
            return 'กำลังโหลด...';
        },

        getUserInitial(userId) {
            const name = this.getUserName(userId);
            return name.charAt(0) || '?';
        },

        async fetchReviews() {
            this.loading = true;
            this.error = null;

            try {
                // Use the correct reviews endpoint with appropriate pagination
                const response = await axios.get('http://127.0.0.1:8000/reviews/all', {
                    params: {
                        skip: 0,
                        limit: 50 // Fetch exact number needed for display
                    }
                });

                // Sort reviews by created_at (newest first)
                this.reviews = Array.isArray(response.data)
                    ? response.data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                    : [];

                console.log('Reviews loaded:', this.reviews.length);

                // Fetch user data for all reviews
                const userIds = [...new Set(this.reviews.map(review => review.user_id))];
                userIds.forEach(userId => {
                    this.fetchUser(userId);
                });
            } catch (err) {
                console.error('Error fetching reviews:', err);
                this.reviews = []; // Initialize as empty array on error
                this.error = 'ไม่สามารถโหลดข้อมูลรีวิวได้ กรุณาลองใหม่อีกครั้ง';
                this.loading = false;
            } finally {
                this.loading = false;
            }
        },

        getProductName(productId) {
            if (!productId) return 'ไม่ระบุชื่อสินค้า';

            const product = this.products.find(p => p.id === productId);
            return product ? product.name : 'ไม่ระบุชื่อสินค้า';
        },

        getProductImage(productId) {
            if (!productId) return this.noImagePlaceholder;

            const product = this.products.find(p => p.id === productId);
            return (product && product.images && product.images.length > 0)
                ? product.images[0]
                : this.noImagePlaceholder;
        },

        formatDate(dateString) {
            if (!dateString) return '';

            const date = new Date(dateString);
            return new Intl.DateTimeFormat('th-TH', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            }).format(date);
        },

        changePage(page) {
            if (page > 0 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },

        editReview(review) {
            this.reviewToEdit = review;
            this.formData = {
                rating: review.rating,
                comment: review.comment,
                status: review.status
            };
            this.showEditModal = true;
        },

        closeModal() {
            this.showEditModal = false;
        },

        async saveReview() {
            try {
                const response = await axios.put(`http://localhost:8000/reviews/${this.reviewToEdit.id}`, {
                    rating: this.formData.rating,
                    comment: this.formData.comment,
                    status: this.formData.status
                });

                // Update local review data
                const index = this.reviews.findIndex(r => r.id === this.reviewToEdit.id);
                if (index !== -1) {
                    this.reviews[index] = response.data;
                }

                this.closeModal();
                alert('บันทึกการแก้ไขรีวิวเรียบร้อยแล้ว');
            } catch (err) {
                console.error('Error saving review:', err);
                alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่อีกครั้ง');
            }
        },

        confirmDeleteReview(review) {
            this.reviewToDelete = review;
            this.showDeleteModal = true;
        },

        async deleteReview() {
            try {
                await axios.delete(`http://localhost:8000/reviews/${this.reviewToDelete.id}`);

                // Remove from local data
                this.reviews = this.reviews.filter(r => r.id !== this.reviewToDelete.id);

                this.showDeleteModal = false;
                alert('ลบรีวิวเรียบร้อยแล้ว');
            } catch (err) {
                console.error('Error deleting review:', err);
                alert('เกิดข้อผิดพลาดในการลบข้อมูล กรุณาลองใหม่อีกครั้ง');
            }
        },

        getStatusName(status) {
            switch (status) {
                case 'approved':
                    return 'อนุมัติแล้ว';
                case 'pending':
                    return 'รอตรวจสอบ';
                case 'rejected':
                    return 'ไม่อนุมัติ';
                default:
                    return '';
            }
        },

        async approveReview(review) {
            try {
                await axios.put(`http://127.0.0.1:8000/reviews/${review.id}/status`, {
                    status: 'approved'
                });

                // Update local data
                const index = this.reviews.findIndex(r => r.id === review.id);
                if (index !== -1) {
                    this.reviews[index].status = 'approved';
                }
            } catch (err) {
                console.error('Error updating review status:', err);
                alert('เกิดข้อผิดพลาดในการอัพเดทสถานะ กรุณาลองใหม่อีกครั้ง');
            }
        },

        async rejectReview(review) {
            try {
                await axios.put(`http://127.0.0.1:8000/reviews/${review.id}/status`, {
                    status: 'rejected'
                });

                // Update local data
                const index = this.reviews.findIndex(r => r.id === review.id);
                if (index !== -1) {
                    this.reviews[index].status = 'rejected';
                }
            } catch (err) {
                console.error('Error updating review status:', err);
                alert('เกิดข้อผิดพลาดในการอัพเดทสถานะ กรุณาลองใหม่อีกครั้ง');
            }
        },

        openImageModal(image) {
            // Implement image modal logic here
        }
    }
};
</script>

<style scoped>
.reviews-management
{
    width: 100%;
}

.page-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

h1
{
    margin: 0;
    color: #2c3e50;
}

.filter-section
{
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.search-box
{
    flex-grow: 1;
    min-width: 200px;
}

.search-box input
{
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.filter-box
{
    display: flex;
    gap: 10px;
}

.filter-box select
{
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    min-width: 150px;
}

.loading-container,
.error-container
{
    padding: 50px;
    text-align: center;
}

.loading-spinner
{
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-left-color: #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 15px;
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

.retry-button
{
    background-color: #3498db;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
}

.reviews-container
{
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}

.review-card
{
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    padding: 20px;
    position: relative;
}

.review-header
{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 15px;
}

.user-info
{
    display: flex;
    align-items: center;
}

.user-avatar
{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #3498db;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 10px;
}

.user-name
{
    font-weight: 600;
    margin-bottom: 5px;
}

.review-date
{
    font-size: 12px;
    color: #7f8c8d;
}

.review-actions
{
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-badge
{
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
}

.status-badge.approved
{
    background-color: #2ecc71;
    color: white;
}

.status-badge.pending
{
    background-color: #f39c12;
    color: white;
}

.status-badge.rejected
{
    background-color: #e74c3c;
    color: white;
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
    font-size: 18px;
    color: #7f8c8d;
}

.dropdown-menu
{
    position: absolute;
    top: 100%;
    right: 0;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    display: none;
    flex-direction: column;
    gap: 5px;
    padding: 10px;
    z-index: 10;
}

.dropdown:hover .dropdown-menu
{
    display: flex;
}

.dropdown-menu button
{
    background: none;
    border: none;
    cursor: pointer;
    font-size: 15px;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 12px;
    width: 100%;
    text-align: left;
}

.dropdown-menu button:hover
{
    background-color: #f5f5f5;
}

.review-product
{
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
}

.product-image img
{
    width: 60px;
    height: 60px;
    border-radius: 4px;
    object-fit: cover;
}

.product-info
{
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.product-name
{
    font-weight: 600;
    color: #2c3e50;
}

.rating
{
    display: flex;
    align-items: center;
    gap: 5px;
}

.stars
{
    display: flex;
    gap: 2px;
}

.stars .fas
{
    color: #ddd;
    font-size: 14px;
}

.stars .filled
{
    color: #f39c12;
}

.rating-value
{
    font-weight: 600;
    color: #f39c12;
}

.review-content
{
    margin-bottom: 20px;
}

.review-title
{
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 5px;
}

.review-text
{
    line-height: 1.5;
    color: #2c3e50;
}

.review-images
{
    display: flex;
    gap: 10px;
}

.review-image
{
    width: 60px;
    height: 60px;
    border-radius: 4px;
    object-fit: cover;
    cursor: pointer;
}

.empty-state
{
    text-align: center;
    padding: 40px;
    background-color: #f9f9f9;
    border-radius: 8px;
    color: #7f8c8d;
}

.pagination
{
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 30px;
}

.pagination button
{
    padding: 8px 12px;
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.pagination button:disabled
{
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination button:hover:not(:disabled)
{
    background-color: #eee;
}

/* Modal Styles - Same as other admin pages */
.modal-overlay
{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
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
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    width: 500px;
    max-width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.delete-modal
{
    width: 400px;
}

.modal-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
}

.modal-header h2
{
    margin: 0;
    font-size: 20px;
}

.close-button
{
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #aaa;
}

.modal-body
{
    padding: 20px;
}

.modal-footer
{
    padding: 15px 20px;
    border-top: 1px solid #eee;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.form-group
{
    margin-bottom: 15px;
}

.form-group label
{
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
}

.rating-select
{
    display: flex;
    gap: 5px;
}

.rating-select .star
{
    font-size: 24px;
}

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
    resize: vertical;
}

.cancel-button,
.save-button,
.delete-button
{
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    border: none;
}

.cancel-button
{
    background-color: #f5f5f5;
    color: #333;
}

.save-button
{
    background-color: #4CAF50;
    color: white;
}

.delete-button
{
    background-color: #e74c3c;
    color: white;
}

.warning
{
    color: #e74c3c;
    font-weight: 500;
}
</style>
