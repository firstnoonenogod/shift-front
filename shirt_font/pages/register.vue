<template>
    <div class="container">
        <header class="header">
            <div class="logo" @click="$router.push('/')">ShirtShop</div>
        </header>

        <div class="register-container">
            <div class="register-card">
                <h1>สมัครสมาชิก</h1>
                <p class="subtitle">กรุณากรอกข้อมูลต่อไปนี้เพื่อสมัครสมาชิก</p>

                <div class="register-form">
                    <div class="form-group" :class="{ error: errors.email }">
                        <label>อีเมล <span class="required">*</span></label>
                        <input type="email" v-model="form.email" placeholder="name@example.com"
                            @focus="removeError('email')" @blur="validateEmail">
                        <span class="error-text" v-if="errors.email">{{ errors.email }}</span>
                    </div>

                    <div class="form-group" :class="{ error: errors.password }">
                        <label>รหัสผ่าน <span class="required">*</span></label>
                        <div class="password-input">
                            <input :type="showPassword ? 'text' : 'password'" v-model="form.password"
                                placeholder="รหัสผ่านอย่างน้อย 8 ตัว" @focus="removeError('password')"
                                @blur="validatePassword">
                            <button type="button" class="toggle-password" @click="showPassword = !showPassword">
                                {{ showPassword ? '👁️' : '👁️‍🗨️' }}
                            </button>
                        </div>
                        <span class="error-text" v-if="errors.password">{{ errors.password }}</span>
                        <div class="password-strength" v-if="form.password">
                            <div class="strength-bar">
                                <div class="strength-level" :style="{ width: passwordStrength.percent + '%' }"
                                    :class="passwordStrength.class"></div>
                            </div>
                            <span class="strength-text" :class="passwordStrength.class">
                                {{ passwordStrength.text }}
                            </span>
                        </div>
                    </div>

                    <div class="form-group" :class="{ error: errors.confirmPassword }">
                        <label>ยืนยันรหัสผ่าน <span class="required">*</span></label>
                        <div class="password-input">
                            <input :type="showConfirmPassword ? 'text' : 'password'" v-model="form.confirmPassword"
                                placeholder="กรอกรหัสผ่านอีกครั้ง" @focus="removeError('confirmPassword')"
                                @blur="validateConfirmPassword">
                            <button type="button" class="toggle-password"
                                @click="showConfirmPassword = !showConfirmPassword">
                                {{ showConfirmPassword ? '👁️' : '👁️‍🗨️' }}
                            </button>
                        </div>
                        <span class="error-text" v-if="errors.confirmPassword">{{ errors.confirmPassword }}</span>
                    </div>

                    <div class="form-group" :class="{ error: errors.phone }">
                        <label>เบอร์โทรศัพท์ <span class="required">*</span></label>
                        <input type="tel" v-model="form.phone" placeholder="0xxxxxxxxx" @focus="removeError('phone')"
                            @blur="validatePhone" maxlength="10">
                        <span class="error-text" v-if="errors.phone">{{ errors.phone }}</span>
                    </div>

                    <div class="form-group" :class="{ error: errors.address }">
                        <label>ที่อยู่ <span class="required">*</span></label>
                        <textarea v-model="form.address" placeholder="กรุณากรอกที่อยู่" @focus="removeError('address')"
                            @blur="validateAddress"></textarea>
                        <span class="error-text" v-if="errors.address">{{ errors.address }}</span>
                    </div>

                    <div class="form-row">
                        <div class="form-group half" :class="{ error: errors.province }">
                            <label>จังหวัด <span class="required">*</span></label>
                            <select v-model="form.province" @focus="removeError('province')" @blur="validateProvince">
                                <option value="">เลือกจังหวัด</option>
                                <option v-for="province in provinces" :key="province" :value="province">
                                    {{ province }}
                                </option>
                            </select>
                            <span class="error-text" v-if="errors.province">{{ errors.province }}</span>
                        </div>

                        <div class="form-group half" :class="{ error: errors.postalCode }">
                            <label>รหัสไปรษณีย์ <span class="required">*</span></label>
                            <input type="text" v-model="form.postalCode" placeholder="รหัสไปรษณีย์"
                                @focus="removeError('postalCode')" @blur="validatePostalCode" maxlength="5">
                            <span class="error-text" v-if="errors.postalCode">{{ errors.postalCode }}</span>
                        </div>
                    </div>

                    <div class="terms-checkbox">
                        <input type="checkbox" id="terms" v-model="form.agreeTerms">
                        <label for="terms">
                            ฉันยอมรับ <a href="#" @click.prevent="showTerms = true">เงื่อนไขการใช้งาน</a> และ
                            <a href="#" @click.prevent="showPrivacy = true">นโยบายความเป็นส่วนตัว</a>
                        </label>
                        <span class="error-text" v-if="errors.agreeTerms">{{ errors.agreeTerms }}</span>
                    </div>

                    <button class="register-button" @click="register" :disabled="isSubmitting || !form.agreeTerms">
                        <span v-if="!isSubmitting">สมัครสมาชิก</span>
                        <span v-else>
                            <span class="loading-spinner"></span>
                            กำลังดำเนินการ...
                        </span>
                    </button>

                    <div class="login-link">
                        มีบัญชีอยู่แล้ว? <a href="#" @click.prevent="$router.push('/login')">เข้าสู่ระบบ</a>
                    </div>

                    <div class="social-register">
                        <p>หรือสมัครสมาชิกด้วย</p>
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

        <!-- Registration Success Modal -->
        <div class="modal-overlay" v-if="showSuccessModal">
            <div class="modal-content">
                <div class="success-icon">✓</div>
                <h3>สมัครสมาชิกสำเร็จ</h3>
                <p>ขอบคุณสำหรับการสมัครสมาชิก</p>
                <button class="continue-button" @click="goToLogin">
                    เข้าสู่ระบบ
                </button>
            </div>
        </div>

        <!-- Terms Modal -->
        <div class="modal-overlay" v-if="showTerms">
            <div class="modal-content terms-content">
                <div class="modal-header">
                    <h3>เงื่อนไขการใช้งาน</h3>
                    <button class="close-button" @click="showTerms = false">×</button>
                </div>
                <div class="modal-body">
                    <div class="terms-text">
                        <h4>1. การยอมรับเงื่อนไข</h4>
                        <p>การใช้บริการของเราถือว่าคุณได้อ่านและยอมรับเงื่อนไขการใช้งานทั้งหมด</p>

                        <h4>2. บัญชีผู้ใช้</h4>
                        <p>คุณต้องรับผิดชอบในการรักษาความปลอดภัยของบัญชีและรหัสผ่านของคุณ</p>

                        <h4>3. การสั่งซื้อและชำระเงิน</h4>
                        <p>เราขอสงวนสิทธิ์ในการปฏิเสธการสั่งซื้อหากมีข้อสงสัยเกี่ยวกับความถูกต้องหรือความปลอดภัย</p>

                        <h4>4. การจัดส่ง</h4>
                        <p>เวลาในการจัดส่งเป็นเพียงการประมาณการและอาจมีการเปลี่ยนแปลงได้</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="close-modal-button" @click="showTerms = false">
                        ปิด
                    </button>
                </div>
            </div>
        </div>

        <!-- Privacy Modal -->
        <div class="modal-overlay" v-if="showPrivacy">
            <div class="modal-content terms-content">
                <div class="modal-header">
                    <h3>นโยบายความเป็นส่วนตัว</h3>
                    <button class="close-button" @click="showPrivacy = false">×</button>
                </div>
                <div class="modal-body">
                    <div class="terms-text">
                        <h4>1. ข้อมูลที่เราเก็บ</h4>
                        <p>เราเก็บข้อมูลส่วนบุคคลเช่น ชื่อ อีเมล เบอร์โทร และที่อยู่เพื่อการจัดส่งสินค้า</p>

                        <h4>2. วิธีการใช้ข้อมูล</h4>
                        <p>เราใช้ข้อมูลของคุณเพื่อจัดการคำสั่งซื้อ ปรับปรุงบริการ และติดต่อสื่อสาร</p>

                        <h4>3. การเปิดเผยข้อมูล</h4>
                        <p>เราไม่ขายหรือแบ่งปันข้อมูลส่วนบุคคลของคุณกับบุคคลที่สาม ยกเว้นเพื่อการจัดส่งสินค้า</p>

                        <h4>4. ความปลอดภัยของข้อมูล</h4>
                        <p>เราใช้มาตรการทางเทคนิคและการจัดการที่เหมาะสมเพื่อปกป้องข้อมูลของคุณ</p>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="close-modal-button" @click="showPrivacy = false">
                        ปิด
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ZipCodeUtil from '~/plugins/zipcode.js';

export default {
    data() {
        return {
            form: {
                email: '',
                password: '',
                confirmPassword: '',
                phone: '',
                address: '',
                province: '',
                postalCode: '',
                agreeTerms: false
            },
            errors: {
                email: '',
                password: '',
                confirmPassword: '',
                phone: '',
                address: '',
                province: '',
                postalCode: '',
                agreeTerms: ''
            },
            isSubmitting: false,
            showSuccessModal: false,
            showPassword: false,
            showConfirmPassword: false,
            showTerms: false,
            showPrivacy: false,
            provinces: [
                'กรุงเทพมหานคร', 'เชียงใหม่', 'นครราชสีมา', 'ขอนแก่น', 'เชียงราย', 'อุบลราชธานี',
                'สงขลา', 'นครสวรรค์', 'ชลบุรี', 'อุดรธานี', 'ภูเก็ต', 'สุราษฎร์ธานี', 'ปทุมธานี',
                'นนทบุรี', 'สมุทรปราการ', 'นครปฐม', 'ยะลา', 'นครศรีธรรมราช', 'ประจวบคีรีขันธ์',
                'พระนครศรีอยุธยา'
            ]
        };
    },
    computed: {
        passwordStrength() {
            const password = this.form.password;
            if (!password) {
                return { percent: 0, class: '', text: '' };
            }

            let strength = 0;
            let feedback = '';

            // Check password length
            if (password.length >= 8) strength += 25;

            // Check for mixed case
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 25;

            // Check for numbers
            if (password.match(/\d/)) strength += 25;

            // Check for special characters
            if (password.match(/[^a-zA-Z\d]/)) strength += 25;

            // Determine strength text and class
            if (strength <= 25) {
                feedback = 'รหัสผ่านอ่อนแอ';
                return { percent: 25, class: 'weak', text: feedback };
            } else if (strength <= 50) {
                feedback = 'รหัสผ่านปานกลาง';
                return { percent: 50, class: 'medium', text: feedback };
            } else if (strength <= 75) {
                feedback = 'รหัสผ่านดี';
                return { percent: 75, class: 'good', text: feedback };
            } else {
                feedback = 'รหัสผ่านแข็งแรงมาก';
                return { percent: 100, class: 'strong', text: feedback };
            }
        }
    },
    methods: {
        validateEmail() {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!this.form.email) {
                this.errors.email = 'กรุณากรอกอีเมล';
                return false;
            } else if (!emailRegex.test(this.form.email)) {
                this.errors.email = 'รูปแบบอีเมลไม่ถูกต้อง';
                return false;
            }
            return true;
        },

        validatePassword() {
            if (!this.form.password) {
                this.errors.password = 'กรุณากรอกรหัสผ่าน';
                return false;
            } else if (this.form.password.length < 8) {
                this.errors.password = 'รหัสผ่านต้องมีอย่างน้อย 8 ตัวอักษร';
                return false;
            }
            return true;
        },

        validateConfirmPassword() {
            if (!this.form.confirmPassword) {
                this.errors.confirmPassword = 'กรุณายืนยันรหัสผ่าน';
                return false;
            } else if (this.form.password !== this.form.confirmPassword) {
                this.errors.confirmPassword = 'รหัสผ่านไม่ตรงกัน';
                return false;
            }
            return true;
        },

        validatePhone() {
            const phoneRegex = /^0\d{9}$/;
            if (!this.form.phone) {
                this.errors.phone = 'กรุณากรอกเบอร์โทรศัพท์';
                return false;
            } else if (!phoneRegex.test(this.form.phone)) {
                this.errors.phone = 'รูปแบบเบอร์โทรศัพท์ไม่ถูกต้อง';
                return false;
            }
            return true;
        },

        validateAddress() {
            if (!this.form.address) {
                this.errors.address = 'กรุณากรอกที่อยู่';
                return false;
            }
            return true;
        },

        validateProvince() {
            if (!this.form.province) {
                this.errors.province = 'กรุณาเลือกจังหวัด';
                return false;
            }
            return true;
        },

        validatePostalCode() {
            const postalCodeRegex = /^\d{5}$/;
            if (!this.form.postalCode) {
                this.errors.postalCode = 'กรุณากรอกรหัสไปรษณีย์';
                return false;
            } else if (!postalCodeRegex.test(this.form.postalCode)) {
                this.errors.postalCode = 'รหัสไปรษณีย์ไม่ถูกต้อง';
                return false;
            }

            // Auto-fill province from zipcode if found
            this.autoFillFromZipcode(this.form.postalCode);
            return true;
        },

        autoFillFromZipcode(zipcode) {
            const addressInfo = ZipCodeUtil.getAddressInfo(zipcode);
            if (addressInfo) {
                this.form.province = addressInfo.province;
                // Display success notice
                this.$nextTick(() => {
                    const notification = document.createElement('div');
                    notification.className = 'auto-fill-notification';
                    notification.textContent = 'ข้อมูลจังหวัดถูกเติมโดยอัตโนมัติ';
                    document.body.appendChild(notification);

                    setTimeout(() => {
                        notification.classList.add('show');
                        setTimeout(() => {
                            notification.classList.remove('show');
                            setTimeout(() => {
                                document.body.removeChild(notification);
                            }, 300);
                        }, 2000);
                    }, 100);
                });
            }
        },

        validateTerms() {
            if (!this.form.agreeTerms) {
                this.errors.agreeTerms = 'กรุณายอมรับเงื่อนไขการใช้งาน';
                return false;
            }
            return true;
        },

        removeError(field) {
            this.errors[field] = '';
        },

        validateForm() {
            let isValid = true;

            if (!this.validateEmail()) isValid = false;
            if (!this.validatePassword()) isValid = false;
            if (!this.validateConfirmPassword()) isValid = false;
            if (!this.validatePhone()) isValid = false;
            if (!this.validateAddress()) isValid = false;
            if (!this.validateProvince()) isValid = false;
            if (!this.validatePostalCode()) isValid = false;
            if (!this.validateTerms()) isValid = false;

            return isValid;
        },

        // Improved register method with success animation
        register() {
            if (this.validateForm()) {
                this.isSubmitting = true;

                // Simulate API call with progress
                let progress = 0;
                const interval = setInterval(() => {
                    progress += 10;
                    if (progress >= 100) {
                        clearInterval(interval);
                        this.isSubmitting = false;
                        this.showSuccessModal = true;

                        // Save user data to localStorage (for demo purposes only)
                        localStorage.setItem('user', JSON.stringify({
                            email: this.form.email,
                            phone: this.form.phone,
                            address: this.form.address,
                            province: this.form.province,
                            postalCode: this.form.postalCode,
                            role: 'consumer'
                        }));
                    }
                }, 200);
            }
        },

        goToLogin() {
            this.$router.push('/login');
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

.register-container
{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 0 0 60px;
}

.register-card
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 600px;
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

.form-row
{
    display: flex;
    gap: 15px;
}

.half
{
    flex: 1;
}

.form-group.error input,
.form-group.error textarea,
.form-group.error select
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

.required
{
    color: #ff4d4f;
}

label
{
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #333;
}

input,
textarea,
select
{
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
    transition: border-color 0.3s;
}

input:focus,
textarea:focus,
select:focus
{
    outline: none;
    border-color: #ee4d2d;
}

textarea
{
    min-height: 100px;
    resize: vertical;
}

select
{
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%23333' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 12px center;
    padding-right: 32px;
}

.password-input
{
    position: relative;
}

.toggle-password
{
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    color: #999;
    font-size: 16px;
    padding: 0;
}

.password-strength
{
    margin-top: 8px;
}

.strength-bar
{
    height: 4px;
    background-color: #f0f0f0;
    border-radius: 2px;
    overflow: hidden;
}

.strength-level
{
    height: 100%;
    transition: width 0.3s;
}

.strength-level.weak
{
    background-color: #f5222d;
}

.strength-level.medium
{
    background-color: #faad14;
}

.strength-level.good
{
    background-color: #52c41a;
}

.strength-level.strong
{
    background-color: #1890ff;
}

.strength-text
{
    font-size: 12px;
    margin-top: 4px;
    display: block;
}

.strength-text.weak
{
    color: #f5222d;
}

.strength-text.medium
{
    color: #faad14;
}

.strength-text.good
{
    color: #52c41a;
}

.strength-text.strong
{
    color: #1890ff;
}

.terms-checkbox
{
    display: flex;
    align-items: flex-start;
    margin-bottom: 20px;
    gap: 8px;
}

.terms-checkbox input
{
    width: auto;
    margin-top: 4px;
}

.terms-checkbox a
{
    color: #ee4d2d;
    text-decoration: none;
}

.register-button
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
    position: relative;
}

.register-button:hover
{
    background-color: #d73211;
}

.register-button:disabled
{
    background-color: #cccccc;
    cursor: not-allowed;
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

.loading-spinner
{
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    animation: spin 1s infinite linear;
    margin-right: 8px;
    vertical-align: middle;
}

.login-link
{
    text-align: center;
    margin-top: 20px;
    color: #666;
}

.login-link a
{
    color: #ee4d2d;
    text-decoration: none;
    font-weight: 600;
}

/* Social login */
.social-register
{
    margin-top: 30px;
    text-align: center;
}

.social-register p
{
    color: #999;
    margin-bottom: 15px;
    position: relative;
}

.social-register p::before,
.social-register p::after
{
    content: "";
    position: absolute;
    top: 50%;
    width: 35%;
    height: 1px;
    background-color: #eee;
}

.social-register p::before
{
    left: 0;
}

.social-register p::after
{
    right: 0;
}

.social-buttons
{
    display: flex;
    gap: 15px;
}

.social-button
{
    flex: 1;
    padding: 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
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
    background-color: white;
    border: 1px solid #ddd;
    color: #555;
}

.fa-facebook,
.fa-google
{
    font-family: Arial;
    font-weight: bold;
    font-style: normal;
    font-size: 18px;
}

/* Modal styles */
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
    background-color: white;
    border-radius: 8px;
    padding: 30px;
    width: 90%;
    max-width: 400px;
    text-align: center;
}

.modal-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #f0f0f0;
}

.modal-header h3
{
    margin: 0;
}

.terms-content
{
    text-align: left;
    max-width: 600px;
    max-height: 80vh;
    display: flex;
    flex-direction: column;
    padding: 0;
}

.modal-body
{
    padding: 20px;
    max-height: 60vh;
    overflow-y: auto;
}

.modal-footer
{
    padding: 15px 20px;
    border-top: 1px solid #f0f0f0;
    text-align: right;
}

.terms-text h4
{
    margin: 20px 0 10px;
    color: #333;
}

.terms-text p
{
    margin-bottom: 15px;
    color: #666;
    line-height: 1.5;
}

.success-icon
{
    width: 60px;
    height: 60px;
    margin: 0 auto 20px;
    border-radius: 50%;
    background-color: #4caf50;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 30px;
}

.continue-button,
.close-modal-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    margin-top: 20px;
}

/* Auto-fill notification */
.auto-fill-notification
{
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: rgba(76, 175, 80, 0.9);
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.3s, transform 0.3s;
    z-index: 1100;
}

.auto-fill-notification.show
{
    opacity: 1;
    transform: translateY(0);
}

/* Responsive design */
@media (max-width: 768px)
{
    .form-row
    {
        flex-direction: column;
        gap: 0;
    }

    .half
    {
        width: 100%;
    }

    .register-card
    {
        padding: 20px;
    }

    .social-buttons
    {
        flex-direction: column;
    }
}
</style>
