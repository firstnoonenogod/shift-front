<template>
    <div class="container">
        <header class="header">
            <div class="logo" @click="$router.push('/')">ShirtShop</div>
        </header>

        <div class="login-container">
            <div class="login-card">
                <h1>เข้าสู่ระบบ</h1>
                <p class="subtitle">ยินดีต้อนรับกลับมา!</p>

                <div class="login-form">
                    <div class="form-group" :class="{ error: errors.email }">
                        <label>อีเมล</label>
                        <input type="email" v-model="form.email" placeholder="name@example.com">
                        <span class="error-text" v-if="errors.email">{{ errors.email }}</span>
                    </div>

                    <div class="form-group" :class="{ error: errors.password }">
                        <label>รหัสผ่าน</label>
                        <input type="password" v-model="form.password" placeholder="รหัสผ่าน">
                        <span class="error-text" v-if="errors.password">{{ errors.password }}</span>
                    </div>

                    <div class="forgot-password">
                        <a href="#" @click.prevent="forgotPassword">ลืมรหัสผ่าน?</a>
                    </div>

                    <button class="login-button" @click="login" :disabled="isSubmitting">
                        <span v-if="!isSubmitting">เข้าสู่ระบบ</span>
                        <span v-else>กำลังดำเนินการ...</span>
                    </button>

                    <div class="register-link">
                        ยังไม่มีบัญชี? <a href="#" @click.prevent="$router.push('/register')">สมัครสมาชิก</a>
                    </div>

                    <div class="social-login">
                        <p>หรือเข้าสู่ระบบด้วย</p>
                        <div class="social-buttons">
                            <button class="social-button facebook">
                                <i class="fa-facebook">f</i>
                                Facebook
                            </button>
                            <button class="social-button google">
                                <i class="fa-google">G</i>
                                Google
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            form: {
                email: '',
                password: ''
            },
            errors: {
                email: '',
                password: ''
            },
            isSubmitting: false
        };
    },
    methods: {
        validateForm() {
            let isValid = true;
            this.errors = {
                email: '',
                password: ''
            };

            // Validate email
            if (!this.form.email) {
                this.errors.email = 'กรุณากรอกอีเมล';
                isValid = false;
            }

            // Validate password
            if (!this.form.password) {
                this.errors.password = 'กรุณากรอกรหัสผ่าน';
                isValid = false;
            }

            return isValid;
        },

        login() {
            if (this.validateForm()) {
                this.isSubmitting = true;

                // For demo purposes, let's simulate authentication
                setTimeout(() => {
                    this.isSubmitting = false;

                    // Normally we would validate credentials with an API
                    // For demo, check if user exists in localStorage
                    const storedUser = localStorage.getItem('user');
                    if (storedUser) {
                        const user = JSON.parse(storedUser);
                        if (user.email === this.form.email) {
                            // Set login status
                            localStorage.setItem('isLoggedIn', 'true');
                            this.$router.push('/');
                            return;
                        }
                    }

                    // If credentials don't match or user doesn't exist
                    this.errors.email = 'อีเมลหรือรหัสผ่านไม่ถูกต้อง';
                }, 1000);
            }
        },

        forgotPassword() {
            alert('ระบบจะส่งลิงก์สำหรับตั้งรหัสผ่านใหม่ไปยังอีเมลของคุณ');
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
    justify-content: center;
    padding: 20px 0;
}

.logo
{
    font-size: 24px;
    font-weight: bold;
    color: #ee4d2d;
    cursor: pointer;
}

.login-container
{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0 60px;
    min-height: 60vh;
}

.login-card
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
    padding: 30px;
}

h1
{
    text-align: center;
    color: #333;
    margin-bottom: 8px;
}

.subtitle
{
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

.form-group
{
    margin-bottom: 20px;
}

.form-group.error input
{
    border-color: #ff4d4f;
}

.error-text
{
    color: #ff4d4f;
    font-size: 14px;
    margin-top: 4px;
    display: block;
}

label
{
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #333;
}

input
{
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
}

input:focus
{
    outline: none;
    border-color: #ee4d2d;
}

.forgot-password
{
    text-align: right;
    margin-bottom: 20px;
}

.forgot-password a
{
    color: #ee4d2d;
    text-decoration: none;
    font-size: 14px;
}

.login-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
    margin-top: 10px;
    transition: background-color 0.3s;
}

.login-button:hover
{
    background-color: #d73211;
}

.login-button:disabled
{
    background-color: #cccccc;
    cursor: not-allowed;
}

.register-link
{
    text-align: center;
    margin-top: 20px;
    color: #666;
}

.register-link a
{
    color: #ee4d2d;
    text-decoration: none;
    font-weight: 600;
}

.social-login
{
    margin-top: 30px;
    text-align: center;
}

.social-login p
{
    color: #999;
    margin-bottom: 15px;
    position: relative;
}

.social-login p::before,
.social-login p::after
{
    content: "";
    position: absolute;
    top: 50%;
    width: 35%;
    height: 1px;
    background-color: #eee;
}

.social-login p::before
{
    left: 0;
}

.social-login p::after
{
    right: 0;
}

.social-buttons
{
    display: flex;
    gap: 10px;
}

.social-button
{
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: opacity 0.3s;
}

.social-button:hover
{
    opacity: 0.9;
}

.social-button.facebook
{
    background-color: #3b5998;
    color: white;
}

.social-button.google
{
    background-color: #fff;
    border: 1px solid #ddd;
    color: #555;
}

.fa-facebook,
.fa-google
{
    font-family: Arial;
    font-weight: bold;
    font-style: normal;
    font-size: 16px;
}
</style>
