<template>
    <AdminLayout>
        <div class="categories-management">
            <div class="page-header">
                <h1>จัดการหมวดหมู่</h1>
                <button class="add-button" @click="openAddModal">+ เพิ่มหมวดหมู่ใหม่</button>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <p>{{ error }}</p>
                <button @click="fetchCategories" class="retry-button">ลองใหม่</button>
            </div>

            <div v-else>
                <div class="table-container">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>รหัส</th>
                                <th>ชื่อหมวดหมู่</th>
                                <th>คำอธิบาย</th>
                                <th>จำนวนสินค้า</th>
                                <th>การจัดการ</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="category in categories" :key="category.id">
                                <td>{{ category.id }}</td>
                                <td>{{ category.name }}</td>
                                <td>{{ category.description || '-' }}</td>
                                <td>{{ category.product_count || 0 }}</td>
                                <td class="actions">
                                    <button class="edit-btn" @click="editCategory(category)" title="แก้ไข">
                                        <i class="fas fa-edit"></i>
                                    </button>
                                    <button class="delete-btn" @click="confirmDeleteCategory(category)" title="ลบ">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    <div v-if="categories.length === 0" class="empty-state">
                        <i class="fas fa-folder-open fa-3x"></i>
                        <p>ยังไม่มีหมวดหมู่ กรุณาเพิ่มหมวดหมู่ใหม่</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add/Edit Category Modal -->
        <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>{{ isEditing ? 'แก้ไขหมวดหมู่' : 'เพิ่มหมวดหมู่ใหม่' }}</h2>
                    <button class="close-button" @click="closeModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-group">
                        <label for="categoryName">ชื่อหมวดหมู่</label>
                        <input type="text" id="categoryName" v-model="formData.name" required>
                    </div>
                    <div class="form-group">
                        <label for="categoryDescription">คำอธิบาย</label>
                        <textarea id="categoryDescription" v-model="formData.description" rows="4"></textarea>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeModal">ยกเลิก</button>
                    <button class="save-button" @click="saveCategory">บันทึก</button>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal">
                <div class="modal-header">
                    <h2>ยืนยันการลบหมวดหมู่</h2>
                    <button class="close-button" @click="closeDeleteModal">&times;</button>
                </div>
                <div class="modal-body">
                    <p>คุณต้องการลบหมวดหมู่ "{{ categoryToDelete.name }}" ใช่หรือไม่?</p>
                    <p class="warning" v-if="categoryToDelete.product_count > 0">
                        หมวดหมู่นี้มีสินค้าอยู่ {{ categoryToDelete.product_count }} รายการ
                        การลบหมวดหมู่อาจส่งผลต่อสินค้าเหล่านี้
                    </p>
                    <p class="warning">การลบรายการนี้จะไม่สามารถกู้คืนได้</p>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeDeleteModal">ยกเลิก</button>
                    <button class="delete-button" @click="deleteCategory">ยืนยันการลบ</button>
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
            categories: [],
            loading: false,
            error: null,
            showModal: false,
            showDeleteModal: false,
            isEditing: false,
            formData: {
                name: '',
                description: ''
            },
            categoryToDelete: {}
        };
    },
    mounted() {
        this.fetchCategories();
    },
    methods: {
        async fetchCategories() {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.get('http://localhost:8000/categories/');
                this.categories = response.data;
                this.loading = false;
            } catch (err) {
                this.error = 'ไม่สามารถโหลดข้อมูลหมวดหมู่ได้';
                this.loading = false;
                console.error('Error fetching categories:', err);
            }
        },

        openAddModal() {
            this.isEditing = false;
            this.formData = {
                name: '',
                description: ''
            };
            this.showModal = true;
        },

        editCategory(category) {
            this.isEditing = true;
            this.formData = {
                id: category.id,
                name: category.name,
                description: category.description || ''
            };
            this.showModal = true;
        },

        closeModal() {
            this.showModal = false;
        },

        confirmDeleteCategory(category) {
            this.categoryToDelete = category;
            this.showDeleteModal = true;
        },

        closeDeleteModal() {
            this.showDeleteModal = false;
        },

        async saveCategory() {
            try {
                // Validate form data
                if (!this.formData.name.trim()) {
                    alert('กรุณากรอกชื่อหมวดหมู่');
                    return;
                }

                // Prepare payload
                const payload = {
                    name: this.formData.name,
                    description: this.formData.description
                };

                if (this.isEditing) {
                    // Update existing category
                    await axios.put(`http://localhost:8000/categories/${this.formData.id}`, payload);

                    // Update local data
                    const index = this.categories.findIndex(c => c.id === this.formData.id);
                    if (index !== -1) {
                        this.categories[index] = {
                            ...this.categories[index],
                            ...payload
                        };
                    }

                    alert('อัพเดทหมวดหมู่เรียบร้อยแล้ว');
                } else {
                    // Create new category
                    const response = await axios.post('http://localhost:8000/categories/', payload);

                    // Add to local data
                    this.categories.unshift({
                        ...response.data,
                        product_count: 0
                    });

                    alert('เพิ่มหมวดหมู่ใหม่เรียบร้อยแล้ว');
                }

                this.closeModal();
            } catch (err) {
                console.error('Error saving category:', err);
                alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล');
            }
        },

        async deleteCategory() {
            try {
                // Delete category
                await axios.delete(`http://localhost:8000/categories/${this.categoryToDelete.id}`);

                // Update local data
                this.categories = this.categories.filter(c => c.id !== this.categoryToDelete.id);
                this.closeDeleteModal();
                alert('ลบหมวดหมู่เรียบร้อยแล้ว');
            } catch (err) {
                console.error('Error deleting category:', err);
                alert('เกิดข้อผิดพลาดในการลบหมวดหมู่');
            }
        }
    }
};
</script>

<style scoped>
.categories-management
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

.actions
{
    display: flex;
    gap: 10px;
}

.edit-btn,
.delete-btn
{
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    color: white;
    font-size: 16px;
}

.edit-btn
{
    background-color: #ff9800;
}

.delete-btn
{
    background-color: #f44336;
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

.empty-state
{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 50px 0;
    color: #aaa;
}

.empty-state i
{
    margin-bottom: 20px;
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

.form-group
{
    margin-bottom: 15px;
}

.form-group label
{
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

.form-group input,
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
.delete-button
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

.warning
{
    color: #f44336;
    font-weight: 500;
}
</style>
