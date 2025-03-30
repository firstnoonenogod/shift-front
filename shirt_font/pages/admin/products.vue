<template>
    <AdminLayout>
        <div class="products-management">
            <div class="page-header">
                <h1>จัดการสินค้า</h1>
                <button class="add-button" @click="openAddModal">+ เพิ่มสินค้าใหม่</button>
            </div>

            <div class="filter-section">
                <div class="search-box">
                    <input type="text" v-model="searchQuery" placeholder="ค้นหาสินค้า..." />
                </div>
                <div class="filter-box">
                    <select v-model="categoryFilter">
                        <option value="">ทุกหมวดหมู่</option>
                        <option v-for="category in categories" :key="category.id" :value="category.id">
                            {{ category.name }}
                        </option>
                    </select>
                    <select v-model="statusFilter">
                        <option value="">ทุกสถานะ</option>
                        <option value="active">ใช้งาน</option>
                        <option value="inactive">ปิดใช้งาน</option>
                    </select>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <p>{{ error }}</p>
                <button @click="fetchProducts" class="retry-button">ลองใหม่</button>
            </div>

            <div v-else>
                <!-- Product Grid View -->
                <div v-if="viewMode === 'grid'" class="products-grid">
                    <div v-for="product in paginatedProducts" :key="product.id" class="product-card">
                        <div class="product-image">
                            <img :src="getProductImage(product)" :alt="product.name">
                            <!-- <div class="product-status" :class="product.status"> -->
                            <!-- {{ product.status === 'active' ? 'ใช้งาน' : 'ปิดใช้งาน' }} -->
                            <!-- </div> -->
                            <div class="product-actions">
                                <button @click.stop="viewProductDetails(product)" title="ดู">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button @click.stop="editProduct(product)" title="แก้ไข">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button @click.stop="confirmDeleteProduct(product)" title="ลบ">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                        <div class="product-info">
                            <h3 class="product-name">{{ product.name }}</h3>
                            <p class="product-category">{{ getCategoryName(product.category_id) }}</p>
                            <div class="product-price-stock">
                                <div class="product-price">฿{{ formatPrice(product.price) }}</div>
                                <div class="product-stock">สต็อก: {{ product.stock }}</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Product List View -->
                <div v-else class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th class="image-cell">รูปภาพ</th>
                                <th>ชื่อสินค้า</th>
                                <th>หมวดหมู่</th>
                                <th>ราคา</th>
                                <th>สต็อก</th>
                                <th>สถานะ</th>
                                <th>การจัดการ</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="product in paginatedProducts" :key="product.id">
                                <td class="image-cell">
                                    <img :src="getProductImage(product)" :alt="product.name" class="product-thumbnail">
                                </td>
                                <td>{{ product.name }}</td>
                                <td>{{ getCategoryName(product.category_id) }}</td>
                                <td>฿{{ formatPrice(product.price) }}</td>
                                <td>{{ product.stock }}</td>
                                <td>
                                    <span class="status-badge" :class="product.status">
                                        {{ product.status === 'active' ? 'ใช้งาน' : 'ปิดใช้งาน' }}
                                    </span>
                                </td>
                                <td class="actions">
                                    <button class="view-btn" @click="viewProductDetails(product)" title="ดู">
                                        <i class="fas fa-eye"></i>
                                    </button>
                                    <button class="edit-btn" @click="editProduct(product)" title="แก้ไข">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="delete-btn" @click="confirmDeleteProduct(product)" title="ลบ">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- View Mode Toggle and Pagination -->
                <div class="view-controls">
                    <div class="view-toggle">
                        <button :class="{ 'active': viewMode === 'grid' }" @click="viewMode = 'grid'" title="Grid View">
                            <i class="fas fa-th"></i>
                        </button>
                        <button :class="{ 'active': viewMode === 'list' }" @click="viewMode = 'list'" title="List View">
                            <i class="fas fa-list"></i>
                        </button>
                    </div>

                    <div class="pagination" v-if="totalPages > 1">
                        <button :disabled="currentPage === 1" @click="changePage(currentPage - 1)">
                            &laquo; ก่อนหน้า
                        </button>
                        <span>หน้า {{ currentPage }} จาก {{ totalPages }}</span>
                        <button :disabled="currentPage === totalPages" @click="changePage(currentPage + 1)">
                            ถัดไป &raquo;
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add/Edit Product Modal -->
        <div v-if="showModal" class="modal-overlay">
            <div class="modal-content large-modal">
                <div class="modal-header">
                    <h2>{{ isEditing ? 'แก้ไขสินค้า' : 'เพิ่มสินค้าใหม่' }}</h2>
                    <button class="close-button" @click="closeModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="productName">ชื่อสินค้า</label>
                            <input type="text" id="productName" v-model="formData.name" required>
                        </div>

                        <div class="form-group">
                            <label for="productCategory">หมวดหมู่</label>
                            <select id="productCategory" v-model="formData.category_id" required>
                                <option value="">เลือกหมวดหมู่</option>
                                <option v-for="category in categories" :key="category.id" :value="category.id">
                                    {{ category.name }}
                                </option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="productPrice">ราคา</label>
                            <input type="number" id="productPrice" v-model.number="formData.price" min="0" step="0.01"
                                required>
                        </div>

                        <div class="form-group">
                            <label for="productStock">จำนวนในสต็อก</label>
                            <input type="number" id="productStock" v-model.number="formData.stock" min="0" step="1"
                                required>
                        </div>

                        <div class="form-group">
                            <label for="productStatus">สถานะ</label>
                            <select id="productStatus" v-model="formData.status">
                                <option value="active">ใช้งาน</option>
                                <option value="inactive">ปิดใช้งาน</option>
                            </select>
                        </div>

                        <div class="form-group full-width">
                            <label for="productDescription">รายละเอียดสินค้า</label>
                            <textarea id="productDescription" v-model="formData.description" rows="4"></textarea>
                        </div>

                        <div class="form-group full-width">
                            <label>รูปภาพสินค้า</label>
                            <div class="image-url-input">
                                <input type="text" v-model="imageUrl" placeholder="ใส่ URL รูปภาพ">
                                <button class="add-image-button" @click="addImage">เพิ่มรูปภาพ</button>
                            </div>
                            <div class="image-preview-container" v-if="formData.images && formData.images.length > 0">
                                <div class="image-preview" v-for="(image, index) in formData.images" :key="index">
                                    <img :src="image" alt="Product Preview">
                                    <button class="remove-image" @click="removeImage(index)">&times;</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeModal">ยกเลิก</button>
                    <button class="save-button" @click="saveProduct">บันทึก</button>
                </div>
            </div>
        </div>

        <!-- View Product Details Modal -->
        <div v-if="showViewModal" class="modal-overlay">
            <div class="modal-content large-modal">
                <div class="modal-header">
                    <h2>รายละเอียดสินค้า</h2>
                    <button class="close-button" @click="closeViewModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="product-detail-view">
                        <div class="product-detail-image">
                            <img :src="getProductImage(selectedProduct)" :alt="selectedProduct.name">
                        </div>
                        <div class="product-detail-info">
                            <h3>{{ selectedProduct.name }}</h3>
                            <div class="info-grid">
                                <div class="info-row">
                                    <div class="label">หมวดหมู่</div>
                                    <div>{{ getCategoryName(selectedProduct.category_id) }}</div>
                                </div>
                                <div class="info-row">
                                    <div class="label">ราคา</div>
                                    <div class="price">฿{{ formatPrice(selectedProduct.price) }}</div>
                                </div>
                                <div class="info-row">
                                    <div class="label">จำนวนในสต็อก</div>
                                    <div>{{ selectedProduct.stock }}</div>
                                </div>
                                <div class="info-row">
                                    <div class="label">สถานะ</div>
                                    <div>
                                        <span class="status-badge" :class="selectedProduct.status">
                                            {{ selectedProduct.status === 'active' ? 'ใช้งาน' : 'ปิดใช้งาน' }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="description-section">
                                <h4>รายละเอียดสินค้า</h4>
                                <p>{{ selectedProduct.description || 'ไม่มีรายละเอียดสินค้า' }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeViewModal">ปิด</button>
                    <button class="edit-button" @click="editFromView">แก้ไข</button>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal">
                <div class="modal-header">
                    <h2>ยืนยันการลบสินค้า</h2>
                    <button class="close-button" @click="closeDeleteModal">&times;</button>
                </div>
                <div class="modal-body">
                    <p>คุณต้องการลบสินค้า "{{ productToDelete.name }}" ใช่หรือไม่?</p>
                    <p class="warning">การลบรายการนี้จะไม่สามารถกู้คืนได้</p>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeDeleteModal">ยกเลิก</button>
                    <button class="delete-button" @click="deleteProduct">ยืนยันการลบ</button>
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
            products: [],
            categories: [],
            loading: false,
            error: null,
            searchQuery: '',
            categoryFilter: '',
            statusFilter: '',
            viewMode: 'grid',
            currentPage: 1,
            itemsPerPage: 12,
            showModal: false,
            showViewModal: false,
            showDeleteModal: false,
            isEditing: false,
            imageUrl: '',
            formData: {
                name: '',
                category_id: '',
                price: 0,
                stock: 0,
                status: 'active',
                images: [],
                description: ''
            },
            selectedProduct: {},
            productToDelete: {},
            noImagePlaceholder: null,
        };
    },
    computed: {
        filteredProducts() {
            let result = this.products;

            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                result = result.filter(product =>
                    product.name.toLowerCase().includes(query) ||
                    (product.description && product.description.toLowerCase().includes(query))
                );
            }

            if (this.categoryFilter) {
                result = result.filter(product => product.category_id === this.categoryFilter);
            }

            if (this.statusFilter) {
                result = result.filter(product => product.status === this.statusFilter);
            }

            return result;
        },
        paginatedProducts() {
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            return this.filteredProducts.slice(startIndex, startIndex + this.itemsPerPage);
        },
        totalPages() {
            return Math.max(1, Math.ceil(this.filteredProducts.length / this.itemsPerPage));
        }
    },
    mounted() {
        this.fetchProducts();
        this.fetchCategories();
        // Create placeholder for no image
        try {
            this.noImagePlaceholder = getProductPlaceholder(300, 300, 'No Image');
        } catch (e) {
            // Fallback for SSR where canvas might not be available
            this.noImagePlaceholder = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiB2aWV3Qm94PSIwIDAgMjAwIDIwMCI+PHJlY3Qgd2lkdGg9IjIwMCIgaGVpZ2h0PSIyMDAiIGZpbGw9IiNlMmUyZTIiLz48dGV4dCB4PSI1MCUiIHk9IjUwJSIgZG9taW5hbnQtYmFzZWxpbmU9Im1pZGRsZSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9Im1vbm9zcGFjZSIgZm9udC1zaXplPSIyNnB4IiBmaWxsPSIjOTk5OTk5Ij5ObyBJbWFnZTwvdGV4dD48L3N2Zz4=';
        }
    },
    methods: {
        async fetchProducts() {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get('http://localhost:8000/products/');
                this.products = response.data;
                this.loading = false;
            } catch (err) {
                this.error = 'ไม่สามารถโหลดข้อมูลสินค้าได้';
                this.loading = false;
                console.error('Error fetching products:', err);
            }
        },

        async fetchCategories() {
            try {
                const response = await axios.get('http://localhost:8000/categories/');
                this.categories = response.data;
            } catch (err) {
                console.error('Error fetching categories:', err);
                this.error = 'ไม่สามารถโหลดข้อมูลหมวดหมู่ได้';
            }
        },

        getCategoryName(categoryId) {
            const category = this.categories.find(c => c.id === categoryId);
            return category ? category.name : 'ไม่มีหมวดหมู่';
        },

        formatPrice(price) {
            return Number(price).toLocaleString('th-TH');
        },

        changePage(page) {
            if (page > 0 && page <= this.totalPages) {
                this.currentPage = page;
            }
        },

        viewProductDetails(product) {
            this.selectedProduct = { ...product };
            this.showViewModal = true;
        },

        closeViewModal() {
            this.showViewModal = false;
        },

        openAddModal() {
            this.isEditing = false;
            this.formData = {
                name: '',
                category_id: '',
                price: 0,
                stock: 0,
                status: 'active',
                images: [],
                description: ''
            };
            this.imageUrl = '';
            this.showModal = true;
        },

        editProduct(product) {
            this.isEditing = true;
            this.formData = {
                ...product,
                images: product.images || []
            };
            this.imageUrl = '';
            this.showModal = true;
        },

        editFromView() {
            this.closeViewModal();
            this.editProduct(this.selectedProduct);
        },

        closeModal() {
            this.showModal = false;
        },

        confirmDeleteProduct(product) {
            this.productToDelete = product;
            this.showDeleteModal = true;
        },

        closeDeleteModal() {
            this.showDeleteModal = false;
        },

        addImage() {
            if (this.imageUrl && this.imageUrl.trim() !== '') {
                this.formData.images.push(this.imageUrl.trim());
                this.imageUrl = '';
            }
        },

        removeImage(index) {
            this.formData.images.splice(index, 1);
        },

        getProductImage(product) {
            return product.images && product.images.length > 0 ? product.images[0] : this.noImagePlaceholder;
        },

        async saveProduct() {
            try {
                // Validate form
                if (!this.formData.name || !this.formData.category_id) {
                    alert('กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน');
                    return;
                }

                // Prepare payload for API
                const payload = {
                    name: this.formData.name,
                    description: this.formData.description || '',
                    price: Number(this.formData.price),
                    stock: Number(this.formData.stock),
                    category_id: this.formData.category_id,
                    images: this.formData.images,
                    status: this.formData.status
                };

                if (this.isEditing) {
                    // Update existing product via API
                    await axios.put(`http://localhost:8000/products/${this.formData.id}`, payload);

                    // Update local data
                    const index = this.products.findIndex(p => p.id === this.formData.id);
                    if (index !== -1) {
                        this.products[index] = {
                            ...this.products[index],
                            ...payload
                        };
                    }
                    alert('อัพเดตสินค้าเรียบร้อยแล้ว');
                } else {
                    // Create new product via API
                    const response = await axios.post('http://localhost:8000/products/', payload);

                    // Add to local data
                    this.products.unshift(response.data);
                    alert('เพิ่มสินค้าใหม่เรียบร้อยแล้ว');
                }

                this.closeModal();
            } catch (err) {
                console.error('Error saving product:', err);
                alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล');
            }
        },

        async deleteProduct() {
            try {
                // Delete via API
                await axios.delete(`http://localhost:8000/products/${this.productToDelete.id}`);

                // Update local data
                this.products = this.products.filter(p => p.id !== this.productToDelete.id);
                this.closeDeleteModal();

                // Check if we need to adjust the current page
                if (this.currentPage > this.totalPages && this.currentPage > 1) {
                    this.currentPage = this.totalPages;
                }

                alert('ลบสินค้าเรียบร้อยแล้ว');
            } catch (err) {
                console.error('Error deleting product:', err);
                alert('เกิดข้อผิดพลาดในการลบสินค้า');
            }
        }
    }
};
</script>

<style scoped>
.products-management
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

.add-button
{
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s;
}

.add-button:hover
{
    background-color: #45a049;
}

.filter-section
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
    flex-wrap: wrap;
    gap: 10px;
}

.search-box
{
    flex-grow: 1;
    max-width: 500px;
}

.search-box input
{
    width: 100%;
    padding: 10px 15px;
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
    padding: 10px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    min-width: 150px;
}

/* Image preview styles */
.add-image-button
{
    margin-top: 10px;
    padding: 8px 15px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.image-preview-container
{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
}

.image-preview
{
    position: relative;
    width: 100px;
    height: 100px;
    border: 1px solid #ddd;
    border-radius: 4px;
    overflow: hidden;
}

.image-preview img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.remove-image
{
    position: absolute;
    top: 5px;
    right: 5px;
    background: rgba(255, 0, 0, 0.7);
    color: white;
    border: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

/* Existing styles */
.products-grid
{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.product-card
{
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.product-card:hover
{
    transform: translateY(-5px);
}

.product-image
{
    position: relative;
    height: 200px;
}

.product-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.product-actions
{
    position: absolute;
    top: 10px;
    right: 10px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    opacity: 0;
    transition: opacity 0.2s;
}

.product-card:hover .product-actions
{
    opacity: 1;
}

.product-actions button
{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: none;
    background-color: rgba(255, 255, 255, 0.8);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
}

.product-actions button:hover
{
    background-color: white;
}

.product-status
{
    position: absolute;
    bottom: 10px;
    left: 10px;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.product-status.active
{
    background-color: rgba(76, 175, 80, 0.9);
    color: white;
}

.product-status.inactive
{
    background-color: rgba(244, 67, 54, 0.9);
    color: white;
}

/* Rest of the existing styles */
.product-info
{
    padding: 15px;
}

.product-name
{
    margin: 0 0 8px;
    font-size: 16px;
    font-weight: 600;
}

.product-category
{
    color: #777;
    margin: 0 0 10px;
    font-size: 14px;
}

.product-price-stock
{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.product-price
{
    font-weight: bold;
    color: #e53935;
}

.product-stock
{
    font-size: 14px;
    color: #777;
}

.table-container
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin-bottom: 30px;
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
    background-color: #f9f9f9;
    font-weight: 600;
}

.image-cell
{
    width: 60px;
}

.product-thumbnail
{
    width: 50px;
    height: 50px;
    border-radius: 4px;
    object-fit: cover;
}

.status-badge
{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 20px;
    font-size: 12px;
}

.status-badge.active
{
    background-color: #e8f5e9;
    color: #2e7d32;
}

.status-badge.inactive
{
    background-color: #ffebee;
    color: #c62828;
}

.actions
{
    display: flex;
    gap: 5px;
}

.view-btn,
.edit-btn,
.delete-btn
{
    padding: 6px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    color: white;
}

.view-btn
{
    background-color: #2196F3;
}

.edit-btn
{
    background-color: #ff9800;
}

.delete-btn
{
    background-color: #f44336;
}

.view-controls
{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.view-toggle
{
    display: flex;
    gap: 5px;
}

.view-toggle button
{
    width: 36px;
    height: 36px;
    border-radius: 4px;
    border: 1px solid #ddd;
    background-color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #777;
}

.view-toggle button.active
{
    background-color: #f5f5f5;
    color: #333;
}

.pagination
{
    display: flex;
    align-items: center;
    gap: 15px;
}

.pagination button
{
    padding: 8px 15px;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
}

.pagination button:disabled
{
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination button:not(:disabled):hover
{
    background-color: #f5f5f5;
}

.loading-container,
.error-container
{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100px 0;
    text-align: center;
}

.loading-spinner
{
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    width: 40px;
    height: 40px;
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

.retry-button
{
    background-color: #3498db;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 15px;
}

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
    width: 90%;
    max-width: 500px;
    max-height: 90vh;
    overflow-y: auto;
}

.large-modal
{
    max-width: 800px;
}

.delete-modal
{
    max-width: 400px;
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
    color: #777;
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

.form-grid
{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.form-group
{
    margin-bottom: 15px;
}

.form-group.full-width
{
    grid-column: span 2;
}

.form-group label
{
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea
{
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-family: inherit;
    font-size: 14px;
}

.form-group textarea
{
    resize: vertical;
}

.cancel-button,
.save-button,
.delete-button,
.edit-button
{
    padding: 10px 20px;
    border-radius: 4px;
    border: none;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
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
    background-color: #f44336;
    color: white;
}

.edit-button
{
    background-color: #ff9800;
    color: white;
}

.product-detail-view
{
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 20px;
}

.product-detail-image
{
    height: 300px;
}

.product-detail-image img
{
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 4px;
}

.product-detail-info h3
{
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 22px;
}

.info-grid
{
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
}

.info-row
{
    display: flex;
    justify-content: space-between;
    padding-bottom: 5px;
    border-bottom: 1px dashed #eee;
}

.label
{
    font-weight: 500;
    color: #555;
}

.price
{
    font-weight: bold;
    color: #e53935;
}

.description-section h4
{
    margin-bottom: 10px;
    font-size: 16px;
}

.warning
{
    color: #f44336;
    font-weight: 500;
}

@media (max-width: 768px)
{
    .form-grid
    {
        grid-template-columns: 1fr;
    }

    .form-group.full-width
    {
        grid-column: auto;
    }

    .product-detail-view
    {
        grid-template-columns: 1fr;
    }
}
</style>