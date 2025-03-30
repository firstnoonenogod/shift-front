<template>
  <div class="product-grid">
    <ProductCard v-for="product in products" :key="product.id" :product="product" class="product-grid-item" />
  </div>
</template>

<script>
import ProductCard from '~/components/ProductCard.vue';

export default {
  name: 'ProductGrid',
  components: {
    ProductCard
  },
  props: {
    products: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
.product-grid
{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}

@media (max-width: 768px)
{
  .product-grid
  {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
}
</style>
