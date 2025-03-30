<template>
    <AdminLayout>
        <div class="users-management">
            <div class="page-header">
                <h1>จัดการผู้ใช้</h1>
                <button class="add-button" @click="openAddModal">+ เพิ่มผู้ใช้ใหม่</button>
            </div>

            <div class="filter-section">
                <div class="search-box">
                    <input type="text" v-model="searchQuery" placeholder="ค้นหาผู้ใช้..." />
                </div>
                <div class="filter-box">
                    <select v-model="statusFilter">
                        <option value="">ทุกสถานะ</option>
                        <option value="true">ใช้งาน</option>
                        <option value="false">ระงับใช้งาน</option>
                    </select>
                </div>
            </div>

            <div v-if="loading" class="loading-container">
                <div class="loading-spinner"></div>
                <p>กำลังโหลดข้อมูล...</p>
            </div>

            <div v-else-if="error" class="error-container">
                <p>{{ error }}</p>
                <button @click="fetchUsers" class="retry-button">ลองใหม่</button>
            </div>

            <div v-else class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>รหัส</th>
                            <th>อีเมล</th>
                            <th>ชื่อผู้ใช้</th>
                            <th>ชื่อ-นามสกุล</th>
                            <th>วันที่สมัคร</th>
                            <th>สถานะ</th>
                            <th>การจัดการ</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in filteredUsers" :key="user.id">
                            <td>{{ user.id.substring(0, 8) }}...</td>
                            <td>{{ user.email }}</td>
                            <td>{{ user.username || '-' }}</td>
                            <td>{{ user.full_name || '-' }}</td>
                            <td>{{ formatDate(user.created_at) }}</td>
                            <td>
                                <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                                    {{ user.is_active ? 'ใช้งาน' : 'ระงับใช้งาน' }}
                                </span>
                            </td>
                            <td class="actions">
                                <button class="view-btn" @click="viewUserDetails(user)">
                                    <i class="fas fa-eye"></i>
                                </button>
                                <button class="edit-btn" @click="editUser(user)">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button class="delete-btn" @click="confirmDeleteUser(user)">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>

                <div class="pagination">
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

        <!-- Add/Edit User Modal -->
        <div v-if="showModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>{{ isEditing ? 'แก้ไขข้อมูลผู้ใช้' : 'เพิ่มผู้ใช้ใหม่' }}</h2>
                    <button class="close-button" @click="closeModal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="form-grid">
                        <div class="form-group">
                            <label for="email">อีเมล</label>
                            <input type="email" id="email" v-model="formData.email" required>
                        </div>

                        <div class="form-group">
                            <label for="username">ชื่อผู้ใช้</label>
                            <input type="text" id="username" v-model="formData.username">
                        </div>

                        <div class="form-group">
                            <label for="fullName">ชื่อ-นามสกุล</label>
                            <input type="text" id="fullName" v-model="formData.full_name">
                        </div>

                        <div class="form-group">
                            <label for="status">สถานะ</label>
                            <select id="status" v-model="formData.is_active">
                                <option :value="true">ใช้งาน</option>
                                <option :value="false">ระงับใช้งาน</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label for="password">รหัสผ่าน
                                {{ isEditing ? '(เว้นว่างไว้หากไม่ต้องการเปลี่ยน)' : '' }}</label>
                            <input type="password" id="password" v-model="formData.password" :required="!isEditing">
                        </div>

                        <div class="form-group">
                            <label for="confirmPassword">ยืนยันรหัสผ่าน</label>
                            <input type="password" id="confirmPassword" v-model="formData.confirmPassword"
                                :required="!isEditing">
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-button" @click="closeModal">ยกเลิก</button>
                    <button class="save-button" @click="saveUser">บันทึก</button>
                </div>
            </div>
        </div>

        <!-- View User Details Modal -->
        <div v-if="showViewModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>ข้อมูลผู้ใช้</h2>
                    <button class="close-button" @click="showViewModal = false">&times;</button>
                </div>
                <div class="modal-body user-details">
                    <div class="user-avatar">
                        {{ (selectedUser.username || selectedUser.email)?.charAt(0).toUpperCase() || 'U' }}
                    </div>
                    <div class="user-info-container">
                        <div class="info-row">
                            <span class="label">รหัสผู้ใช้:</span>
                            <span>{{ selectedUser.id }}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">อีเมล:</span>
                            <span>{{ selectedUser.email }}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">ชื่อผู้ใช้:</span>
                            <span>{{ selectedUser.username || '-' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">ชื่อ-นามสกุล:</span>
                            <span>{{ selectedUser.full_name || '-' }}</span>
                        </div>
                        <div class="info-row">
                            <span class="label">สถานะ:</span>
                            <span class="status-badge" :class="selectedUser.is_active ? 'active' : 'inactive'">
                                {{ selectedUser.is_active ? 'ใช้งาน' : 'ระงับใช้งาน' }}
                            </span>
                        </div>
                        <div class="info-row">
                            <span class="label">วันที่สมัคร:</span>
                            <span>{{ formatDate(selectedUser.created_at) }}</span>
                        </div>
                        <div class="info-row" v-if="selectedUser.updated_at">
                            <span class="label">แก้ไขล่าสุด:</span>
                            <span>{{ formatDate(selectedUser.updated_at) }}</span>
                        </div>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="regular-button" @click="showViewModal = false">ปิด</button>
                    <button class="edit-button" @click="editFromView">แก้ไขข้อมูล</button>
                </div>
            </div>
        </div>

        <!-- Delete Confirmation Modal -->
        <div v-if="showDeleteModal" class="modal-overlay">
            <div class="modal-content delete-modal">
                <div class="modal-header">
                    <h2>ยืนยันการลบผู้ใช้</h2>
                    <button class="close-button" @click="closeDeleteModal">&times;</button>
                </div>
                <div class="modal-body">
                    <p>คุณต้องการลบผู้ใช้ "{{ userToDelete.email }}" ใช่หรือไม่?</p>
                    <p class="warning">การลบข้อมูลผู้ใช้จะไม่สามารถกู้คืนได้</p>
                </div>
                <div class="modal-footer">
                    <button class="regular-button" @click="closeDeleteModal">ยกเลิก</button>
                    <button class="delete-button" @click="deleteUser">ยืนยันการลบ</button>
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
            users: [],
            loading: false,
            error: null,
            searchQuery: '',
            statusFilter: '',
            currentPage: 1,
            itemsPerPage: 10,
            showModal: false,
            showViewModal: false,
            showDeleteModal: false,
            isEditing: false,
            formData: {
                email: '',
                username: '',
                full_name: '',
                password: '',
                confirmPassword: '',
                is_active: true
            },
            selectedUser: {},
            userToDelete: {}
        };
    },
    computed: {
        filteredUsers() {
            let result = this.users;

            // Apply search filter
            if (this.searchQuery) {
                const query = this.searchQuery.toLowerCase();
                result = result.filter(user =>
                    user.email.toLowerCase().includes(query) ||
                    (user.username && user.username.toLowerCase().includes(query)) ||
                    (user.full_name && user.full_name.toLowerCase().includes(query))
                );
            }

            // Apply status filter
            if (this.statusFilter !== '') {
                const isActive = this.statusFilter === 'true';
                result = result.filter(user => user.is_active === isActive);
            }

            // Apply pagination
            const startIndex = (this.currentPage - 1) * this.itemsPerPage;
            return result.slice(startIndex, startIndex + this.itemsPerPage);
        },

        totalPages() {
            let filteredCount = this.users.length;

            if (this.searchQuery || this.statusFilter !== '') {
                filteredCount = this.users.filter(user => {
                    let matches = true;

                    if (this.searchQuery) {
                        const query = this.searchQuery.toLowerCase();
                        matches = user.email.toLowerCase().includes(query) ||
                            (user.username && user.username.toLowerCase().includes(query)) ||
                            (user.full_name && user.full_name.toLowerCase().includes(query));
                    }

                    if (matches && this.statusFilter !== '') {
                        const isActive = this.statusFilter === 'true';
                        matches = user.is_active === isActive;
                    }

                    return matches;
                }).length;
            }

            return Math.max(1, Math.ceil(filteredCount / this.itemsPerPage));
        }
    },
    mounted() {
        this.fetchUsers();
    },
    methods: {
        async fetchUsers() {
            this.loading = true;
            this.error = null;

            try {
                const response = await axios.get('http://localhost:8000/users/');
                this.users = response.data;
                this.loading = false;
            } catch (err) {
                console.error('Error fetching users:', err);
                this.error = 'ไม่สามารถโหลดข้อมูลผู้ใช้ได้ กรุณาลองใหม่อีกครั้ง';
                this.loading = false;
            }
        },

        formatDate(dateString) {
            if (!dateString) return '-';

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

        viewUserDetails(user) {
            this.selectedUser = { ...user };
            this.showViewModal = true;
        },

        openAddModal() {
            this.isEditing = false;
            this.formData = {
                email: '',
                username: '',
                full_name: '',
                password: '',
                confirmPassword: '',
                is_active: true
            };
            this.showModal = true;
        },

        editUser(user) {
            this.isEditing = true;
            this.formData = {
                id: user.id,
                email: user.email,
                username: user.username || '',
                full_name: user.full_name || '',
                password: '',
                confirmPassword: '',
                is_active: user.is_active
            };
            this.showModal = true;
        },

        editFromView() {
            this.showViewModal = false;
            this.editUser(this.selectedUser);
        },

        closeModal() {
            this.showModal = false;
        },

        async saveUser() {
            try {
                // Validate form data
                if (!this.formData.email) {
                    alert('กรุณากรอกอีเมล');
                    return;
                }

                if (!this.isEditing && !this.formData.password) {
                    alert('กรุณากรอกรหัสผ่าน');
                    return;
                }

                if (this.formData.password && this.formData.password !== this.formData.confirmPassword) {
                    alert('รหัสผ่านไม่ตรงกัน');
                    return;
                }

                // Create payload for API
                const payload = {
                    email: this.formData.email,
                    username: this.formData.username,
                    full_name: this.formData.full_name,
                    is_active: this.formData.is_active
                };

                if (this.formData.password) {
                    payload.password = this.formData.password;
                }

                if (this.isEditing) {
                    // Update existing user
                    await axios.put(`http://localhost:8000/users/${this.formData.id}`, payload);

                    // Update local data
                    const index = this.users.findIndex(u => u.id === this.formData.id);
                    if (index !== -1) {
                        this.users[index] = {
                            ...this.users[index],
                            ...payload,
                            updated_at: new Date().toISOString()
                        };
                    }

                    alert('อัพเดทข้อมูลผู้ใช้เรียบร้อยแล้ว');
                } else {
                    // Create new user
                    const response = await axios.post('http://localhost:8000/users/register', payload);
                    this.users.unshift(response.data);
                    alert('เพิ่มผู้ใช้ใหม่เรียบร้อยแล้ว');
                }

                this.closeModal();
            } catch (err) {
                console.error('Error saving user:', err);

                if (err.response && err.response.data && err.response.data.detail) {
                    alert(`เกิดข้อผิดพลาด: ${err.response.data.detail}`);
                } else {
                    alert('เกิดข้อผิดพลาดในการบันทึกข้อมูล กรุณาลองใหม่อีกครั้ง');
                }
            }
        },

        confirmDeleteUser(user) {
            this.userToDelete = user;
            this.showDeleteModal = true;
        },

        closeDeleteModal() {
            this.showDeleteModal = false;
        },

        async deleteUser() {
            try {
                await axios.delete(`http://localhost:8000/users/${this.userToDelete.id}`);

                // Update local data
                this.users = this.users.filter(u => u.id !== this.userToDelete.id);
                this.closeDeleteModal();

                // Check if we need to adjust current page
                if (this.currentPage > this.totalPages && this.currentPage > 1) {
                    this.currentPage = this.totalPages;
                }

                alert('ลบผู้ใช้เรียบร้อยแล้ว');
            } catch (err) {
                console.error('Error deleting user:', err);

                if (err.response && err.response.data && err.response.data.detail) {
                    alert(`เกิดข้อผิดพลาด: ${err.response.data.detail}`);
                } else {
                    alert('เกิดข้อผิดพลาดในการลบผู้ใช้ กรุณาลองใหม่อีกครั้ง');
                }
            }
        }
    }
};
</script>

<style scoped>
.users-management
{
    width: 100%;
    padding: 20px;
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

.add-button
{
    background-color: #4caf50;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: background-color 0.2s;
}

.add-button:hover
{
    background-color: #45a049;
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

.table-container
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    overflow: hidden;
}

.data-table
{
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.data-table th,
.data-table td
{
    padding: 12px 15px;
    border-bottom: 1px solid #eee;
}

.data-table th
{
    background-color: #f9f9f9;
    font-weight: 500;
}

.status-badge
{
    display: inline-block;
    padding: 4px 8px;
    border-radius: 12px;
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
    padding: 6px 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    transition: background-color 0.2s;
}

.view-btn
{
    background-color: #e3f2fd;
    color: #1976d2;
}

.edit-btn
{
    background-color: #fff8e1;
    color: #f57f17;
}

.delete-btn
{
    background-color: #ffebee;
    color: #c62828;
}

.view-btn:hover
{
    background-color: #bbdefb;
}

.edit-btn:hover
{
    background-color: #ffecb3;
}

.delete-btn:hover
{
    background-color: #ffcdd2;
}

.pagination
{
    display: flex;
    justify-content: center;
    gap: 15px;
    padding: 20px 0;
    background: white;
    border-top: 1px solid #eee;
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
    background-color: #f5f5f5;
}

/* Modal Styles */
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
    font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea
{
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.cancel-button,
.save-button,
.regular-button,
.edit-button,
.delete-button
{
    padding: 10px 15px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background-color 0.2s;
    border: none;
}

.cancel-button
{
    background-color: #f5f5f5;
    color: #333;
}

.save-button
{
    background-color: #4caf50;
    color: white;
}

.regular-button
{
    background-color: #e0e0e0;
    color: #333;
}

.edit-button
{
    background-color: #ff9800;
    color: white;
}

.delete-button
{
    background-color: #f44336;
    color: white;
}

.user-details
{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.user-avatar
{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: #3498db;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 36px;
    color: white;
    margin-bottom: 20px;
}

.user-info-container
{
    width: 100%;
}

.info-row
{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px dashed #eee;
}

.info-row .label
{
    font-weight: 600;
    color: #333;
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
}
</style>