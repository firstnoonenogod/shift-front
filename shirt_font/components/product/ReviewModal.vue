<template>
  <div class="review-modal-overlay">
    <div class="review-modal">
      <div class="review-modal-header">
        <h2>รีวิวสินค้า</h2>
        <button class="close-button" @click="$emit('close')">×</button>
      </div>

      <div class="review-modal-body">
        <div class="product-preview">
          <img :src="product.image" :alt="product.name" class="product-image">
          <div class="product-info">
            <div class="product-name">{{ product.name }}</div>
            <div class="product-options" v-if="productOptions">{{ productOptions }}</div>
          </div>
        </div>

        <div class="review-form">
          <h3>เราอยากทราบความคิดเห็นของคุณ!</h3>
          <p class="review-instructions">รีวิวของคุณจะช่วยให้ลูกค้าท่านอื่นตัดสินใจซื้อสินค้าได้ง่ายขึ้น</p>

          <div class="rating-selection">
            <p class="rating-label">ให้คะแนนสินค้า:</p>
            <div class="star-rating">
              <span v-for="star in 5" :key="star" class="star-rating-item" :class="{ active: star <= rating }"
                @click="setRating(star)" @mouseover="hoverRating = star" @mouseleave="hoverRating = 0">★</span>
            </div>
            <div class="rating-text">{{ ratingTexts[Math.max(rating || hoverRating, 1) - 1] }}</div>
          </div>

          <div class="comment-input">
            <label for="reviewComment">เขียนความคิดเห็น (ไม่บังคับ):</label>
            <textarea id="reviewComment" v-model="comment"
              placeholder="บอกเราเกี่ยวกับคุณภาพสินค้า การใช้งาน หรือความประทับใจในสินค้า" rows="3"
              maxlength="500"></textarea>
            <div class="character-count">{{ comment.length }}/500</div>
          </div>

          <div class="form-actions">
            <button class="skip-button" @click="$emit('skip')">ข้ามไปก่อน</button>
            <button class="submit-button" :disabled="!rating || isSubmitting" @click="submitReview">
              <span v-if="isSubmitting">กำลังส่ง...</span>
              <span v-else>ส่งรีวิว</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    product: {
      type: Object,
      required: true
    },
    orderId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      rating: 0,
      hoverRating: 0,
      comment: '',
      isSubmitting: false,
      ratingTexts: [
        'แย่มาก',
        'แย่',
        'พอใช้',
        'ดี',
        'ดีมาก'
      ]
    };
  },
  computed: {
    productOptions() {
      const options = [];
      if (this.product.size) options.push(this.product.size);
      if (this.product.color) options.push(this.product.color);
      return options.join(' | ');
    },

    currentUserId() {
      try {
        const userData = JSON.parse(localStorage.getItem('user') || '{}');
        return userData.id;
      } catch (e) {
        return null;
      }
    }
  },
  methods: {
    setRating(value) {
      this.rating = value;
    },

    async submitReview() {
      if (!this.rating) return;

      this.isSubmitting = true;

      try {
        // Simplified review data format matching the API requirements
        const reviewData = {
          product_id: this.product.id,
          rating: this.rating,
          comment: this.comment.trim()
        };

        const response = await axios.post('http://localhost:8000/reviews', reviewData);

        this.$emit('success', response.data);
      } catch (error) {
        console.error('Error submitting review:', error);
        alert('ขออภัย เกิดข้อผิดพลาดในการส่งรีวิว กรุณาลองใหม่ภายหลัง');
      } finally {
        this.isSubmitting = false;
      }
    }
  }
};
</script>

<style scoped>
.review-modal-overlay
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
  z-index: 1100;
}

.review-modal
{
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.review-modal-header
{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.review-modal-header h2
{
  margin: 0;
  color: #333;
  font-size: 20px;
}

.close-button
{
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.review-modal-body
{
  padding: 20px;
}

.product-preview
{
  display: flex;
  align-items: center;
  gap: 15px;
  padding-bottom: 15px;
  margin-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.product-image
{
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}

.product-name
{
  font-weight: 600;
  margin-bottom: 5px;
}

.product-options
{
  color: #666;
  font-size: 14px;
}

.review-form h3
{
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
  font-size: 18px;
}

.review-instructions
{
  color: #666;
  margin-bottom: 20px;
  font-size: 14px;
}

.rating-selection
{
  margin-bottom: 20px;
}

.rating-label
{
  margin-bottom: 8px;
  font-weight: 500;
}

.star-rating
{
  display: flex;
  gap: 8px;
}

.star-rating-item
{
  font-size: 28px;
  cursor: pointer;
  color: #ddd;
  transition: color 0.2s;
}

.star-rating-item:hover,
.star-rating-item.active
{
  color: #ffb400;
}

.rating-text
{
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}

.comment-input
{
  margin-bottom: 20px;
}

.comment-input label
{
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.comment-input textarea
{
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 15px;
  resize: vertical;
}

.character-count
{
  text-align: right;
  margin-top: 5px;
  font-size: 12px;
  color: #999;
}

.form-actions
{
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-top: 20px;
}

.skip-button
{
  background-color: white;
  border: 1px solid #ddd;
  color: #666;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  flex: 1;
  transition: all 0.2s;
}

.skip-button:hover
{
  background-color: #f5f5f5;
}

.submit-button
{
  background-color: #ee4d2d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  flex: 2;
  transition: all 0.2s;
}

.submit-button:hover:not(:disabled)
{
  background-color: #d73211;
}

.submit-button:disabled
{
  background-color: #f5f5f5;
  color: #aaa;
  cursor: not-allowed;
}
</style>
