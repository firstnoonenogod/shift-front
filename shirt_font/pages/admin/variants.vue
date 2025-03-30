<template>
    <AdminLayout>
        <div class="variants-management">
            <div class="page-header">
                <h1>จัดการตัวเลือกสินค้า</h1>
                <button @click="openAddVariantModal" class="add-button">
                    <i class="fas fa-plus"></i> เพิ่มตัวเลือกสินค้า
                </button>
            </div>

            <div class="filter-section">
                <div class="search-box">
                    <input type="text" v-model="searchQuery" placeholder="ค้นหาตัวเลือกสินค้า..." />
                </div>
                <div class="filter-box">
                    <select v-model="productFilter">
                        <option value="">สินค้าทั้งหมด</option>
                        <option v-for="product in products" :key="product.id" :value="product.id">
                            {{ product.name }}
                        </option>
                    </select>
                    <select v-model="sizeFilter">
                        <option value="">ทุกขนาด</option>
                        <option v-for="size in uniqueSizes" :key="size" :value="size">
                            {{ size }}
                        </option>
                    </select>
                    <select v-model="colorFilter">
                        <option value="">ทุกสี</option>
                        <option v-for="color in uniqueColors" :key="color" :value="color">
                            {{ color }}
                        </option>
                    </select>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <p>{{ error }}</p>
                <button @click="fetchVariants" class="retry-button">ลองใหม่</button>
            </div>

            <div v-else>
                <div class="table-container">
                    <table class="variants-table">
                        <thead>
                            <tr>
                                <th>รหัสตัวเลือก</th>
                                <th>สินค้า</th>
                                <th>ขนาด</th>
                                <th>สี</th>
                                <th>ราคา</th>
                                <th>สต็อก</th>
                                <th>การจัดการ</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="variant in filteredVariants" :key="variant.id">
                                <td>{{ variant.id.substring(0, 8) }}...</td>
                                <td>{{ getProductName(variant.product_id) }}</td>
                                <td>{{ variant.size }}</td>
                                <td class="color-cell">
                                    <span class="color-preview"
                                        :style="{ backgroundColor: getColorCode(variant.color) }"></span>
                                    {{ variant.color }}
                                </td>
                                <td>฿{{ formatPrice(variant.price) }}</td>
                                <td>
                                    <span :class="getStockClass(variant.stock)">{{ variant.stock }}</span>
                                </td>
                                <td class="actions">
                                    <button class="edit-button" @click="openEditVariantModal(variant)">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="delete-button" @click="openDeleteVariantModal(variant)">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div v-if="filteredVariants.length === 0" class="empty-state">
                    <i class="fas fa-tags fa-3x"></i>
                    <p>ไม่พบตัวเลือกสินค้า</p>
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

        <!-- Add/Edit Variant Modal -->
        <div v-if="showVariantModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>{{ isEditMode ? 'แก้ไขตัวเลือกสินค้า' : 'เพิ่มตัวเลือกสินค้า' }}</h2>
                    <button class="close-button" @click="closeVariantModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div v-if="formError" class="form-error">
                        <p>{{ formError }}</p>
                    </div>

                    <form @submit.prevent="saveVariant">
                        <div class="form-group">
                            <label for="productId">สินค้า*</label>
                            <select id="productId" v-model="variantForm.product_id" required :disabled="isEditMode">
                                <option value="" disabled>เลือกสินค้า</option>
                                <option v-for="product in products" :key="product.id" :value="product.id">
                                    {{ product.name }}
                                </option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="size">ขนาด*</label>
                            <input type="text" id="size" v-model="variantForm.size" required />
                        </div>
                        <div class="form-group">
                            <label for="color">สี*</label>
                            <input type="text" id="color" v-model="variantForm.color" required />
                        </div>
                        <div class="form-group">
                            <label for="price">ราคา*</label>
                            <input type="number" id="price" v-model.number="variantForm.price" min="0" step="0.01"
                                required />
                        </div>
                        <div class="form-group">
                            <label for="stock">สต็อก*</label>
                            <input type="number" id="stock" v-model.number="variantForm.stock" min="0" required />
                        </div>

                        <div class="modal-footer">
                            <button type="button" class="cancel-button" @click="closeVariantModal">ยกเลิก</button>
                            <button type="submit" class="save-button" :disabled="formSubmitting">
                                {{ formSubmitting ? 'กำลังบันทึก...' : 'บันทึก' }}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal">
                <div class="modal-header">
                    <h2>ยืนยันการลบตัวเลือกสินค้า</h2>
                    <button class="close-button" @click="closeDeleteModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div v-if="deleteError" class="form-error">
                        <p>{{ deleteError }}</p>
                    </div>
                    <p>คุณต้องการลบตัวเลือกสินค้า "{{ variantToDelete.size }} - {{ variantToDelete.color }}" ใช่หรือไม่?
                    </p>
                    <p class="warning">การลบตัวเลือกสินค้าจะไม่สามารถเรียกคืนได้</p>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeDeleteModal">ยกเลิก</button>
                    <button class="delete-button" :disabled="formSubmitting" @click="confirmDeleteVariant">
                        {{ formSubmitting ? 'กำลังลบ...' : 'ลบตัวเลือกสินค้า' }}
                    </button>
                </div>
            </div>
        </div>
    </AdminLayout>
</template>

<script>
import AdminLayout from '~/components/admin/AdminLayout.vue';
import axios from 'axios';

export default {
    components: {
        AdminLayout
    },
    data() {
        return {
            variants: [],
            products: [],
            searchQuery: '',
            productFilter: '',
            sizeFilter: '',
            colorFilter: '',
            currentPage: 1,
            itemsPerPage: 10,
            showVariantModal: false,
            isEditMode: false,
            variantForm: {
                product_id: '',
                size: '',
                color: '',
                price: 0,
                stock: 0
            },
            showDeleteModal: false,
            variantToDelete: {},
            variantToEdit: {},
            loading: false,
            error: null,
            formError: null,
            deleteError: null,
            formSubmitting: false,
            API_URL: 'http://127.0.0.1:8000'
        };
    },
    computed: {
        filteredVariants() {
            let result = this.variants;

            // Apply search filter
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                result = result.filter(variant =>
                    variant.size.toLowerCase().includes(query) ||
                    variant.color.toLowerCase().includes(query) ||
                    this.getProductName(variant.product_id).toLowerCase().includes(query)
                );
            }

            // Apply product filter
            if (this.productFilter) {
                result = result.filter(variant => variant.product_id === this.productFilter);
            }

            // Apply size filter
            if (this.sizeFilter) {
                result = result.filter(variant => variant.size === this.sizeFilter);
            }

            // Apply color filter
            if (this.colorFilter) {
                result = result.filter(variant => variant.color === this.colorFilter);
            }

            // Apply pagination
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            return result.slice(startIndex, startIndex + this.itemsPerPage);
        },
        totalPages() {
            let filteredCount = this.variants.length;

            // Apply filters for count calculation
            if (this.searchQuery || this.productFilter || this.sizeFilter || this.colorFilter) {
                let result = this.variants;

                if (this.searchQuery) {
                    const query = this.searchQuery.toLowerCase();
                    result = result.filter(variant =>
                        variant.size.toLowerCase().includes(query) ||
                        variant.color.toLowerCase().includes(query) ||
                        this.getProductName(variant.product_id).toLowerCase().includes(query)
                    );
                }

                if (this.productFilter) {
                    result = result.filter(variant => variant.product_id === this.productFilter);
                }

                if (this.sizeFilter) {
                    result = result.filter(variant => variant.size === this.sizeFilter);
                }

                if (this.colorFilter) {
                    result = result.filter(variant => variant.color === this.colorFilter);
                }

                filteredCount = result.length;
            }

            return Math.max(1, Math.ceil(filteredCount / this.itemsPerPage));
        },
        uniqueSizes() {
            const sizes = new Set(this.variants.map(variant => variant.size));
            return Array.from(sizes).sort();
        },
        uniqueColors() {
            const colors = new Set(this.variants.map(variant => variant.color));
            return Array.from(colors).sort();
        }
    },
    mounted() {
        this.fetchVariants();
        this.fetchProducts();
    },
    methods: {
        async fetchVariants() {
            this.loading = true;
            this.error = null;

            try {
                const response = await axios.get(`${this.API_URL}/variants/`);
                console.log('Variants response:', response.data);
                this.variants = response.data;
            } catch (err) {
                console.error('Error fetching variants:', err);
                this.error = err.response?.data?.detail || err.message || 'ไม่สามารถโหลดข้อมูลตัวเลือกสินค้าได้';
            } finally {
                this.loading = false;
            }
        },

        async fetchProducts() {
            try {
                const response = await axios.get(`${this.API_URL}/products/`);
                this.products = response.data;
            } catch (err) {
                console.error('Error fetching products:', err);
                this.error = err.response?.data?.detail || err.message || 'ไม่สามารถโหลดข้อมูลสินค้าได้';
            }
        },

        getProductName(productId) {
            const product = this.products.find(p => p.id === productId);
            return product ? product.name : 'ไม่พบสินค้า';
        },

        getColorCode(colorName) {
            // Map Thai color names to hex codes
            const colorMap = {
                'แดง': '#ff0000',
                'เขียว': '#00ff00',
                'น้ำเงิน': '#0000ff',
                'ดำ': '#000000',
                'ขาว': '#ffffff',
                'เหลือง': '#ffff00',
                'ส้ม': '#ffa500',
                'ม่วง': '#800080',
                'ชมพู': '#ffc0cb',
                'น้ำตาล': '#a52a2a',
                'เทา': '#808080'
            };

            return colorMap[colorName] || '#cccccc'; // Default gray if color not found
        },

        getStockClass(stock) {
            if (stock <= 0) return 'stock-out';
            if (stock < 5) return 'stock-low';
            return 'stock-available';
        },

        formatPrice(price) {
            return price.toLocaleString('th-TH');
        },

        changePage(page) {
            this.currentPage = page;
        },

        openAddVariantModal() {
            this.isEditMode = false;
            this.formError = null;
            this.variantForm = {
                product_id: '',
                size: '',
                color: '',
                price: 0,
                stock: 0
            };
            this.showVariantModal = true;
        },

        openEditVariantModal(variant) {
            this.isEditMode = true;
            this.formError = null;
            this.variantForm = {
                product_id: variant.product_id,
                size: variant.size,
                color: variant.color,
                price: variant.price,
                stock: variant.stock
            };
            this.variantToEdit = variant;
            this.showVariantModal = true;
        },

        closeVariantModal() {
            this.showVariantModal = false;
            this.formError = null;
        },

        async saveVariant() {
            // Validate form
            if (!this.variantForm.product_id || !this.variantForm.size || !this.variantForm.color) {
                this.formError = 'กรุณากรอกข้อมูลให้ครบ';
                return;
            }

            // Convert price and stock to numbers
            const price = parseFloat(this.variantForm.price);
            const stock = parseInt(this.variantForm.stock);

            if (isNaN(price) || price < 0) {
                this.formError = 'ราคาต้องเป็นตัวเลขและมากกว่าหรือเท่ากับ 0';
                return;
            }

            if (isNaN(stock) || stock < 0) {
                this.formError = 'สต็อกต้องเป็นตัวเลขและมากกว่าหรือเท่ากับ 0';
                return;
            }

            this.formSubmitting = true;
            this.formError = null;

            try {
                // Create a regular JSON object instead of FormData
                const variantData = {
                    product_id: this.variantForm.product_id,
                    size: this.variantForm.size,
                    color: this.variantForm.color,
                    price: price,
                    stock: stock
                };

                console.log('Sending variant data:', variantData);

                if (this.isEditMode) {
                    // Update existing variant
                    const response = await axios.put(
                        `${this.API_URL}/variants/${this.variantToEdit.id}`,
                        variantData
                    );

                    // Update variant in local array
                    const index = this.variants.findIndex(v => v.id === this.variantToEdit.id);
                    if (index !== -1) {
                        this.variants[index] = response.data;
                    }
                } else {
                    // Create new variant
                    const response = await axios.post(`${this.API_URL}/variants/`, variantData);
                    this.variants.push(response.data);
                }

                this.closeVariantModal();
            } catch (err) {
                console.error('Error saving variant:', err);
                if (err.response && err.response.data) {
                    console.log('Error details:', err.response.data);
                    if (Array.isArray(err.response.data)) {
                        this.formError = err.response.data.map(e => e.msg).join(', ');
                    } else {
                        this.formError = err.response.data.detail || err.message || 'เกิดข้อผิดพลาดในการบันทึกข้อมูล';
                    }
                } else {
                    this.formError = 'เกิดข้อผิดพลาดในการบันทึกข้อมูล';
                }
            } finally {
                this.formSubmitting = false;
            }
        },

        openDeleteVariantModal(variant) {
            this.variantToDelete = variant;
            this.deleteError = null;
            this.showDeleteModal = true;
        },

        closeDeleteModal() {
            this.showDeleteModal = false;
            this.deleteError = null;
        },

        async confirmDeleteVariant() {
            this.formSubmitting = true;
            this.deleteError = null;

            try {
                await axios.delete(`${this.API_URL}/variants/${this.variantToDelete.id}`);

                // Remove variant from local array
                this.variants = this.variants.filter(v => v.id !== this.variantToDelete.id);

                this.closeDeleteModal();
            } catch (err) {
                console.error('Error deleting variant:', err);
                this.deleteError = err.response?.data?.detail || err.message || 'เกิดข้อผิดพลาดในการลบตัวเลือกสินค้า';
            } finally {
                this.formSubmitting = false;
            }
        }
    }
};
</script>

<style scoped>
.variants-management
{
    padding: 20px;
}

.page-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.add-button
{
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px 15px;
    cursor: pointer;
    display: flex;
    align-items: center;
}

.add-button i
{
    margin-right: 5px;
}

.filter-section
{
    display: flex;
    margin-bottom: 20px;
    gap: 15px;
}

.search-box
{
    flex: 1;
}

.search-box input
{
    width: 100%;
    padding: 8px 12px;
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
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.loading-container,
.error-container
{
    text-align: center;
    padding: 40px;
}

.loading-spinner
{
    margin: 0 auto 20px;
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
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
}

.table-container
{
    overflow-x: auto;
}

.variants-table
{
    width: 100%;
    border-collapse: collapse;
}

.variants-table th,
.variants-table td
{
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

.variants-table th
{
    background-color: #f9f9f9;
    font-weight: bold;
}

.color-cell
{
    display: flex;
    align-items: center;
}

.color-preview
{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    margin-right: 8px;
}

.actions
{
    display: flex;
    gap: 5px;
}

.edit-button,
.delete-button
{
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 16px;
}

.edit-button
{
    color: #ff9800;
}

.delete-button
{
    color: #f44336;
}

.empty-state
{
    text-align: center;
    padding: 40px;
    color: #999;
}

.empty-state i
{
    margin-bottom: 15px;
}

.pagination
{
    display: flex;
    justify-content: center;
    gap: 15px;
    padding: 20px;
    border-top: 1px solid #eee;
}

.pagination button
{
    padding: 8px 15px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
    cursor: pointer;
}

.pagination button:disabled
{
    opacity: 0.5;
    cursor: not-allowed;
}

.modal-overlay
{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content
{
    background: white;
    border-radius: 8px;
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.delete-modal
{
    max-width: 450px;
}

.modal-header
{
    padding: 15px 20px;
    border-bottom: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-body
{
    padding: 20px;
}

.modal-footer
{
    padding: 15px 20px;
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: flex-end;
    gap: 10px;
}

.close-button
{
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #777;
}

.form-group
{
    margin-bottom: 20px;
}

.form-group label
{
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group select
{
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.cancel-button,
.save-button,
.delete-button
{
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
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

.warning
{
    color: #f44336;
    font-weight: 500;
}

.stock-out
{
    color: #f44336;
}

.stock-low
{
    color: #ff9800;
}

.stock-available
{
    color: #4CAF50;
}

.form-error
{
    background-color: #ffebee;
    color: #c62828;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 20px;
}
</style>
