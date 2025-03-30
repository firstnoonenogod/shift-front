<template>
    <div class="admin-layout">
        <aside class="sidebar" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
            <div class="logo-container">
                <h2>Shirt Admin</h2>
                <button class="collapse-button" @click="toggleSidebar">
                    <i class="fas" :class="sidebarCollapsed ? 'fa-angle-right' : 'fa-angle-left'"></i>
                </button>
            </div>
            <nav class="main-nav">
                <nuxt-link to="/admin/dashboard" class="nav-item">
                    <i class="fas fa-tachometer-alt"></i>
                    <span v-if="!sidebarCollapsed">แดชบอร์ด</span>
                </nuxt-link>
                <nuxt-link to="/admin/users" class="nav-item">
                    <i class="fas fa-users"></i>
                    <span v-if="!sidebarCollapsed">จัดการผู้ใช้</span>
                </nuxt-link>
                <nuxt-link to="/admin/products" class="nav-item">
                    <i class="fas fa-tshirt"></i>
                    <span v-if="!sidebarCollapsed">จัดการสินค้า</span>
                </nuxt-link>
                <nuxt-link to="/admin/categories" class="nav-item">
                    <i class="fas fa-list"></i>
                    <span v-if="!sidebarCollapsed">จัดการหมวดหมู่</span>
                </nuxt-link>
                <nuxt-link to="/admin/variants" class="nav-item">
                    <i class="fas fa-tags"></i>
                    <span v-if="!sidebarCollapsed">จัดการตัวเลือกสินค้า</span>
                </nuxt-link>
                <nuxt-link to="/admin/reviews" class="nav-item">
                    <i class="fas fa-star"></i>
                    <span v-if="!sidebarCollapsed">จัดการรีวิว</span>
                </nuxt-link>
                <nuxt-link to="/admin/orders" class="nav-item">
                    <i class="fas fa-shopping-cart"></i>
                    <span v-if="!sidebarCollapsed">จัดการออเดอร์</span>
                </nuxt-link>
                <nuxt-link to="/admin/payments" class="nav-item">
                    <i class="fas fa-credit-card"></i>
                    <span v-if="!sidebarCollapsed">จัดการการชำระเงิน</span>
                </nuxt-link>
            </nav>
            <div class="sidebar-footer" v-if="!sidebarCollapsed">
                <div class="admin-info">
                    <div class="admin-avatar">
                        <div class="avatar-placeholder">A</div>
                    </div>
                    <div class="admin-details">
                        <span class="admin-name">แอดมิน</span>
                        <span class="admin-role">ผู้ดูแลระบบ</span>
                    </div>
                </div>
                <button class="logout-button">
                    <i class="fas fa-sign-out-alt"></i> ออกจากระบบ
                </button>
            </div>
        </aside>

        <div class="main-content">
            <header class="admin-header">
                <div class="header-left">
                    <div class="breadcrumb">
                        <span>{{ getCurrentPageName() }}</span>
                    </div>
                </div>
                <div class="header-right">
                    <div class="header-actions">
                        <button class="action-button">
                            <i class="fas fa-bell"></i>
                            <span class="badge">2</span>
                        </button>
                        <button class="action-button">
                            <i class="fas fa-envelope"></i>
                            <span class="badge">5</span>
                        </button>
                        <div class="user-menu">
                            <div class="user-avatar-small">A</div>
                            <span v-if="!sidebarCollapsed" class="user-name">แอดมิน</span>
                        </div>
                    </div>
                </div>
            </header>

            <main class="content-area">
                <slot></slot>
            </main>
        </div>
    </div>
</template>

<script setup>
// Import the admin common styles
import '~/assets/css/admin-common.css';
</script>

<script>
export default {
    name: 'AdminLayout',
    data() {
        return {
            sidebarCollapsed: false
        };
    },
    methods: {
        toggleSidebar() {
            this.sidebarCollapsed = !this.sidebarCollapsed;
        },
        getCurrentPageName() {
            const path = this.$route.path;
            const routes = {
                '/admin/dashboard': 'แดชบอร์ด',
                '/admin/users': 'จัดการผู้ใช้',
                '/admin/products': 'จัดการสินค้า',
                '/admin/categories': 'จัดการหมวดหมู่',
                '/admin/variants': 'จัดการตัวเลือกสินค้า',
                '/admin/reviews': 'จัดการรีวิว',
                '/admin/orders': 'จัดการออเดอร์',
                '/admin/payments': 'จัดการการชำระเงิน'
            };

            return routes[path] || 'หน้าแดชบอร์ด';
        }
    }
};
</script>

<style scoped>
.admin-layout
{
    display: flex;
    min-height: 100vh;
    font-family: 'Prompt', sans-serif;
}

.sidebar
{
    width: 250px;
    background: #2b3a4a;
    color: white;
    display: flex;
    flex-direction: column;
    transition: width 0.3s;
}

.sidebar-collapsed
{
    width: 70px;
}

.logo-container
{
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-collapsed .logo-container
{
    padding: 20px 0;
    justify-content: center;
}

.sidebar-collapsed h2
{
    display: none;
}

.collapse-button
{
    background: none;
    border: none;
    color: white;
    cursor: pointer;
}

.sidebar-collapsed .collapse-button
{
    margin-right: 0;
}

.main-nav
{
    flex-grow: 1;
    padding: 20px 0;
    overflow-y: auto;
}

.nav-item
{
    display: flex;
    align-items: center;
    padding: 12px 20px;
    color: rgba(255, 255, 255, 0.7);
    text-decoration: none;
    transition: all 0.3s;
}

.sidebar-collapsed .nav-item
{
    padding: 12px 0;
    justify-content: center;
}

.nav-item i
{
    margin-right: 10px;
    width: 20px;
    text-align: center;
}

.sidebar-collapsed .nav-item i
{
    margin-right: 0;
}

.nav-item:hover
{
    background: rgba(255, 255, 255, 0.1);
    color: white;
}

.nav-item.nuxt-link-active
{
    background: #3498db;
    color: white;
}

.sidebar-footer
{
    padding: 15px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-info
{
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.admin-avatar
{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    margin-right: 10px;
    background-color: #3498db;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-placeholder
{
    font-size: 20px;
    font-weight: bold;
    color: white;
}

.admin-details
{
    display: flex;
    flex-direction: column;
}

.admin-name
{
    font-weight: bold;
}

.admin-role
{
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
}

.logout-button
{
    background: rgba(255, 255, 255, 0.1);
    border: none;
    color: white;
    padding: 8px;
    width: 100%;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.logout-button i
{
    margin-right: 8px;
}

.main-content
{
    flex-grow: 1;
    background: #f5f7fa;
    display: flex;
    flex-direction: column;
}

.admin-header
{
    height: 64px;
    background: white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 20px;
    z-index: 100;
}

.header-left,
.header-right
{
    display: flex;
    align-items: center;
}

.breadcrumb
{
    color: #555;
    font-size: 16px;
    font-weight: 600;
}

.header-actions
{
    display: flex;
    align-items: center;
}

.action-button
{
    background: none;
    border: none;
    font-size: 18px;
    cursor: pointer;
    color: #555;
    margin-left: 15px;
    position: relative;
}

.badge
{
    position: absolute;
    top: -5px;
    right: -5px;
    background: #e74c3c;
    color: white;
    font-size: 10px;
    width: 16px;
    height: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
}

.user-menu
{
    display: flex;
    align-items: center;
    margin-left: 20px;
    cursor: pointer;
}

.user-avatar-small
{
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin-right: 8px;
    background-color: #3498db;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.user-name
{
    color: #555;
    font-weight: 500;
}

.content-area
{
    flex-grow: 1;
    padding: 20px;
    overflow: auto;
}

@media (max-width: 768px)
{
    .sidebar:not(.sidebar-collapsed)
    {
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        z-index: 1000;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
    }

    .sidebar-collapsed
    {
        width: 0;
        overflow: hidden;
    }

    .main-content
    {
        width: 100%;
    }
}
</style>
