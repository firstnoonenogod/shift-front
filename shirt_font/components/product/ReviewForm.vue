<template>
  <div class="review-form-container">
    <h3 class="review-form-title">แสดงความคิดเห็นต่อสินค้า</h3>

    <div v-if="submitted" class="review-success">
      <div class="success-icon">✓</div>
      <h4>ขอบคุณสำหรับรีวิวของคุณ!</h4>
      <p>ความคิดเห็นของคุณช่วยให้ผู้ซื้อคนอื่น ๆ ตัดสินใจได้ดีขึ้น</p>
      <button class="write-another-btn" @click="resetForm">เขียนรีวิวอีกครั้ง</button>
    </div>

    <form v-else @submit.prevent="submitReview" class="review-form">
      <div class="form-group rating-group">
        <label>ให้คะแนนสินค้านี้</label>
        <div class="rating-stars-container">
          <div class="rating-stars">
            <span v-for="star in 5" :key="star" class="rating-star" :class="{ filled: star <= rating }"
              @click="setRating(star)" @mouseover="hoverRating = star" @mouseleave="hoverRating = 0">
              ★
            </span>
          </div>
          <div class="rating-label">{{ ratingLabel }}</div>
        </div>
        <div v-if="validationErrors.rating" class="error-message">
          {{ validationErrors.rating }}
        </div>
      </div>

      <div class="form-group">
        <label for="review-comment">ข้อความรีวิว (ไม่จำเป็น)</label>
        <textarea id="review-comment" v-model="comment" placeholder="แชร์ประสบการณ์การใช้งานของคุณ..."
          rows="4"></textarea>
        <div v-if="validationErrors.comment" class="error-message">
          {{ validationErrors.comment }}
        </div>
        <div class="character-count" :class="{ 'near-limit': comment.length > 450 }">
          {{ comment.length }}/500 ตัวอักษร
        </div>
      </div>

      <div class="form-actions">
        <button type="submit" class="submit-review-btn" :disabled="isSubmitting">
          <span v-if="isSubmitting" class="spinner"></span>
          <span v-else>ส่งรีวิว</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ReviewForm',
  props: {
    productId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      rating: 0,
      hoverRating: 0,
      comment: '',
      validationErrors: {},
      isSubmitting: false,
      submitted: false
    };
  },
  computed: {
    ratingLabel() {
      const labels = [
        'เลือกคะแนน',
        'แย่มาก',
        'แย่',
        'พอใช้',
        'ดี',
        'ดีมาก'
      ];
      return labels[this.hoverRating || this.rating || 0];
    }
  },
  methods: {
    setRating(value) {
      this.rating = value;
      // Clear validation error if it exists
      if (this.validationErrors.rating) {
        this.validationErrors = { ...this.validationErrors, rating: null };
      }
    },

    validateForm() {
      const errors = {};

      if (!this.rating || this.rating < 1 || this.rating > 5) {
        errors.rating = 'กรุณาให้คะแนนสินค้า';
      }

      if (this.comment && this.comment.length > 500) {
        errors.comment = 'ข้อความรีวิวต้องไม่เกิน 500 ตัวอักษร';
      }

      this.validationErrors = errors;
      return Object.keys(errors).length === 0;
    },

    async submitReview() {
      if (!this.validateForm() || this.isSubmitting) return;

      this.isSubmitting = true;

      try {
        // Create review object
        const review = {
          product_id: this.productId,
          rating: this.rating,
          comment: this.comment || ''
        };

        // For demo purposes, we'll just simulate an API call
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Add created_at date
        review.created_at = new Date().toISOString();

        // Emit the review submitted event with the review data
        this.$emit('review-submitted', review);

        // Mark as submitted to show the success message
        this.submitted = true;
      } catch (error) {
        console.error('Error submitting review:', error);
        alert('เกิดข้อผิดพลาดในการส่งรีวิว กรุณาลองใหม่อีกครั้ง');
      } finally {
        this.isSubmitting = false;
      }
    },

    resetForm() {
      this.rating = 0;
      this.comment = '';
      this.submitted = false;
      this.validationErrors = {};
    }
  }
};
</script>

<style scoped>
.review-form-container
{
  margin-top: 40px;
  padding: 25px;
  border-radius: 8px;
  background-color: #f9f9f9;
  border: 1px solid #eee;
}

.review-form-title
{
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 18px;
}

.form-group
{
  margin-bottom: 20px;
}

.form-group label
{
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.rating-group
{
  margin-bottom: 25px;
}

.rating-stars-container
{
  display: flex;
  align-items: center;
}

.rating-stars
{
  display: flex;
  gap: 5px;
  margin-right: 15px;
}

.rating-star
{
  font-size: 28px;
  color: #e0e0e0;
  cursor: pointer;
  transition: color 0.2s;
}

.rating-star.filled
{
  color: #ffb400;
}

.rating-star:hover
{
  transform: scale(1.1);
}

.rating-label
{
  font-size: 14px;
  color: #666;
}

textarea
{
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
}

textarea:focus
{
  border-color: #ee4d2d;
  outline: none;
}

.character-count
{
  text-align: right;
  margin-top: 5px;
  font-size: 12px;
  color: #999;
}

.character-count.near-limit
{
  color: #ff4d4f;
}

.form-actions
{
  display: flex;
  justify-content: flex-end;
}

.submit-review-btn
{
  padding: 12px 24px;
  background-color: #ee4d2d;
  border: none;
  color: white;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
}

.submit-review-btn:hover:not(:disabled)
{
  background-color: #d73211;
}

.submit-review-btn:disabled
{
  background-color: #f5f5f5;
  color: #aaa;
  cursor: not-allowed;
}

.error-message
{
  color: #ff4d4f;
  font-size: 14px;
  margin-top: 5px;
}

.spinner
{
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
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

.review-success
{
  text-align: center;
  padding: 20px 0;
}

.success-icon
{
  width: 60px;
  height: 60px;
  background-color: #52c41a;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  margin: 0 auto 20px;
}

.write-another-btn
{
  margin-top: 15px;
  padding: 10px 20px;
  background-color: white;
  border: 1px solid #ee4d2d;
  color: #ee4d2d;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.write-another-btn:hover
{
  background-color: rgba(238, 77, 45, 0.05);
}
</style>
