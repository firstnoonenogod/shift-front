<template>
    <div class="product-card" @click="navigateToProduct">
        <div class="product-image">
            <img :src="sanitizedImageUrl" :alt="product.name" @error="handleImageError">
            <div class="discount-tag" v-if="product.discount">-{{ product.discount }}%</div>
        </div>
        <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-price">
                <span class="current-price">฿{{ formatPrice(product.price) }}</span>
                <span class="original-price" v-if="product.originalPrice">฿{{ formatPrice(product.originalPrice)
                    }}</span>
            </div>
            <div class="product-meta">
                <div class="rating">
                    <span class="stars">★</span>
                    {{ product.rating || 0 }}
                </div>
                <div class="sold">ขายแล้ว {{ product.sold || 0 }} ชิ้น</div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    props: {
        product: {
            type: Object,
            required: true
        }
    },
    data ()
    {
        return {
            imageError: false,
            placeholderImage: 'https://via.placeholder.com/300x200?text=No+Image'
        };
    },
    computed: {
        sanitizedImageUrl ()
        {
            // If previous image attempt failed
            if (this.imageError) return this.placeholderImage;

            // First try to access images as array (API response format)
            if (this.product.images && Array.isArray(this.product.images) && this.product.images.length > 0)
            {
                return this.product.images[0]; // Return first image in array
            }

            // Fallback to single image property if exists
            if (this.product.image)
            {
                return this.product.image;
            }

            // Return placeholder if no images available
            return this.placeholderImage;
        }
    },
    methods: {
        navigateToProduct ()
        {
            // Navigate to the product detail page
            this.$router.push(`/product/${this.product.id}`);
        },
        handleImageError ()
        {
            console.log(`Image load error for product: ${this.product.name}`);
            this.imageError = true;
        },
        formatPrice (price)
        {
            // Format large numbers with commas
            return price?.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") || "0";
        }
    }
};
</script>

<style scoped>
.product-card
{
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    background-color: white;
    height: 100%;
    display: flex;
    flex-direction: column;
}

.product-card:hover
{
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.product-image
{
    position: relative;
    height: 200px;
    overflow: hidden;
    padding-top: 100%;
    /* 1:1 Aspect Ratio */
    background-color: #f5f5f5;
}

.product-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
    transition: transform 0.3s;
}

.product-card:hover .product-image img
{
    transform: scale(1.05);
}

.discount-tag
{
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: #ee4d2d;
    color: white;
    padding: 3px 6px;
    border-radius: 2px;
    font-size: 12px;
}

.product-info
{
    padding: 12px;
    flex-grow: 1;
    display: flex;
    flex-direction: column;
}

.product-name
{
    font-size: 14px;
    margin-bottom: 8px;
    color: #333;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    height: 40px;
    line-height: 1.4;
    height: 42px;
    /* Limit to 2 lines */
    overflow: hidden;
    text-overflow: ellipsis;
}

.product-price
{
    display: flex;
    align-items: center;
    margin-bottom: 8px;
}

.current-price
{
    color: #ee4d2d;
    font-size: 16px;
    font-weight: 600;
    margin-right: 8px;
}

.original-price
{
    color: #999;
    font-size: 12px;
    text-decoration: line-through;
    margin-left: 8px;
    font-size: 13px;
}

.product-meta
{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #757575;
}

.rating
{
    display: flex;
    align-items: center;
}

.stars
{
    color: #ee4d2d;
    margin-right: 2px;
    position: relative;
    display: inline-block;
}

.empty-stars
{
    color: #e0e0e0;
    font-size: 14px;
}

.filled-stars
{
    position: absolute;
    top: 0;
    left: 0;
    color: #ffb400;
    overflow: hidden;
    font-size: 14px;
    white-space: nowrap;
}

.rating-count
{
    font-size: 12px;
    color: #999;
    margin-left: 4px;
}
</style>
