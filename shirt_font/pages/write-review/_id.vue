<template>
    <div class="review-page">
        <div class="container">
            <div class="back-link">
                <a @click.prevent="$router.back()">&larr; กลับ</a>
            </div>

            <div class="review-card">
                <h1>เขียนรีวิวสินค้า</h1>

                <div class="product-info">
                    <div class="product-image">
                        <img :src="product.image" :alt="product.name">
                    </div>
                    <div class="product-details">
                        <h3>{{ product.name }}</h3>
                        <p class="product-category">{{ product.category }}</p>
                        <p class="product-price">฿{{ product.price }}</p>
                    </div>
                </div>

                <div class="rating-section">
                    <p>ให้คะแนนสินค้า</p>
                    <div class="stars">
                        <span v-for="n in 5" :key="n" class="star" :class="{ active: n <= rating }"
                            @click="setRating(n)">★</span>
                    </div>
                </div>

                <div class="review-section">
                    <label for="review">ความคิดเห็น</label>
                    <textarea id="review" v-model="reviewText" placeholder="บอกความรู้สึกของคุณเกี่ยวกับสินค้า..."
                        rows="5"></textarea>
                    <div class="char-count" :class="{ warning: reviewText.length > 1000 }">
                        {{ reviewText.length }}/1000
                    </div>
                </div>

                <div class="photo-upload">
                    <p>เพิ่มรูปภาพ (ไม่จำเป็น)</p>
                    <div class="upload-area">
                        <div v-if="!uploadedPhotos.length" @click="triggerFileInput" class="upload-placeholder">
                            <span>+</span>
                            <p>อัพโหลดรูปภาพ</p>
                        </div>
                        <div v-else class="photo-previews">
                            <div v-for="(photo, index) in uploadedPhotos" :key="index" class="photo-preview">
                                <img :src="photo" alt="Preview">
                                <button class="remove-photo" @click="removePhoto(index)">×</button>
                            </div>

                            <div v-if="uploadedPhotos.length < 5" @click="triggerFileInput" class="add-more">
                                <span>+</span>
                            </div>
                        </div>
                        <input type="file" ref="fileInput" style="display: none" accept="image/*"
                            @change="handleFileUpload">
                    </div>
                    <p class="photo-hint">สามารถอัพโหลดได้สูงสุด 5 รูป</p>
                </div>

                <div class="submit-section">
                    <button class="submit-button" :disabled="!isFormValid || isSubmitting" @click="submitReview">
                        {{ isSubmitting ? 'กำลังส่ง...' : 'ส่งรีวิว' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            product: {
                id: '',
                name: 'เสื้อยืดคอกลม',
                category: 'เสื้อยืด',
                price: 350,
                image: 'https://via.placeholder.com/80'
            },
            rating: 0,
            reviewText: '',
            uploadedPhotos: [],
            isSubmitting: false
        };
    },
    computed: {
        isFormValid() {
            return this.rating > 0 && this.reviewText.trim() !== '';
        }
    },
    mounted() {
        // In a real app, you'd fetch the product details based on the ID
        this.product.id = this.$route.params.id;
    },
    methods: {
        setRating(value) {
            this.rating = value;
        },
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        handleFileUpload(event) {
            if (this.uploadedPhotos.length >= 5) {
                alert('คุณสามารถอัพโหลดได้สูงสุด 5 รูปเท่านั้น');
                return;
            }

            const file = event.target.files[0];
            if (!file) return;

            // Create preview URL
            const reader = new FileReader();
            reader.onload = (e) => {
                this.uploadedPhotos.push(e.target.result);
            };
            reader.readAsDataURL(file);

            // Reset the input so the same file can be selected again
            event.target.value = '';
        },
        removePhoto(index) {
            this.uploadedPhotos.splice(index, 1);
        },
        submitReview() {
            if (!this.isFormValid) return;

            this.isSubmitting = true;

            // Simulate API call
            setTimeout(() => {
                this.isSubmitting = false;
                alert('ขอบคุณสำหรับรีวิว!');
                this.$router.push('/orders');
            }, 1500);
        }
    }
};
</script>

<style scoped>
.review-page
{
    padding: 40px 0;
    background-color: #f8f8f8;
}

.back-link
{
    margin-bottom: 20px;
}

.back-link a
{
    color: #555;
    text-decoration: none;
    cursor: pointer;
}

.review-card
{
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
    padding: 30px;
}

h1
{
    text-align: center;
    margin-bottom: 30px;
}

.product-info
{
    display: flex;
    border-bottom: 1px solid #eee;
    padding-bottom: 20px;
    margin-bottom: 20px;
}

.product-image img
{
    width: 80px;
    height: 80px;
    object-fit: cover;
    border-radius: 4px;
}

.product-details
{
    margin-left: 15px;
}

.product-details h3
{
    margin: 0 0 5px 0;
}

.product-category
{
    color: #666;
    font-size: 14px;
    margin: 0 0 5px 0;
}

.product-price
{
    font-weight: bold;
    margin: 0;
}

.rating-section
{
    margin: 20px 0;
}

.stars
{
    display: flex;
    font-size: 30px;
}

.star
{
    color: #ddd;
    cursor: pointer;
    transition: color 0.2s;
}

.star.active
{
    color: #FFD700;
}

.review-section
{
    margin: 20px 0;
}

label
{
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
}

textarea
{
    width: 100%;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    resize: vertical;
    font-family: inherit;
    font-size: 16px;
}

textarea:focus
{
    outline: none;
    border-color: #ee4d2d;
}

.char-count
{
    text-align: right;
    color: #999;
    font-size: 14px;
    margin-top: 5px;
}

.char-count.warning
{
    color: #ff4d4f;
}

.photo-upload
{
    margin: 20px 0;
}

.upload-area
{
    margin-top: 10px;
}

.upload-placeholder
{
    border: 2px dashed #ddd;
    border-radius: 4px;
    height: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.upload-placeholder span
{
    font-size: 30px;
    color: #ddd;
}

.photo-previews
{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.photo-preview
{
    width: 100px;
    height: 100px;
    position: relative;
}

.photo-preview img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
}

.remove-photo
{
    position: absolute;
    top: -10px;
    right: -10px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.6);
    color: white;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

.add-more
{
    width: 100px;
    height: 100px;
    border: 2px dashed #ddd;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
}

.add-more span
{
    font-size: 30px;
    color: #ddd;
}

.photo-hint
{
    color: #999;
    font-size: 14px;
    margin-top: 5px;
}

.submit-section
{
    margin-top: 30px;
    text-align: center;
}

.submit-button
{
    background-color: #ee4d2d;
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 600;
    min-width: 150px;
}

.submit-button:hover
{
    background-color: #d73211;
}

.submit-button:disabled
{
    background-color: #cccccc;
    cursor: not-allowed;
}
</style>
