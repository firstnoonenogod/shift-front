import axios from 'axios';

/**
 * Updates product stock after a purchase by reducing available quantity
 * @param {string} productId - The ID of the product
 * @param {number} purchasedQuantity - The quantity purchased
 * @returns {Promise<number>} - Returns the new stock level
 */
export async function updateProductStock(productId, purchasedQuantity) {
  try {
    // First, get current product data
    const response = await axios.get(`http://127.0.0.1:8000/products/${productId}`);
    const product = response.data;
    
    // Calculate new stock (prevent negative stock)
    const newStock = Math.max(0, product.stock - purchasedQuantity);
    
    // Prepare update payload (keep all existing data, only update stock)
    const updatePayload = {
      name: product.name,
      description: product.description,
      price: product.price,
      stock: newStock,
      category_id: product.category_id,
      images: product.images
    };
    
    // Send PUT request to update the product
    await axios.put(`http://127.0.0.1:8000/products/${productId}`, updatePayload);
    
    console.log(`Stock updated for product ${productId}: ${product.stock} → ${newStock}`);
    return newStock;
  } catch (error) {
    console.error('Error updating product stock:', error);
    throw error;
  }
}

/**
 * Updates stock for all items in an order
 * @param {Array} orderItems - Array of order items with productId and quantity
 * @returns {Promise<void>}
 */
export async function updateStockForOrder(orderItems) {
  try {
    for (const item of orderItems) {
      await updateProductStock(item.productId || item.product_id, item.quantity);
    }
    console.log('All product stocks updated successfully');
  } catch (error) {
    console.error('Error updating stock for order:', error);
    throw error;
  }
}

/**
 * Calculate and update product stock based on sum of its variants
 * @param {string} productId - The product ID to update
 * @returns {Promise<number>} - Returns the total stock across all variants
 */
export async function recalculateProductStock(productId) {
  try {
    // Get all variants for this product
    const variantsResponse = await axios.get(`http://127.0.0.1:8000/variants/product/${productId}`);
    const variants = variantsResponse.data;
    
    // Sum up the stock of all variants
    const totalStock = variants.reduce((sum, variant) => sum + (variant.stock || 0), 0);
    
    // Get current product data
    const productResponse = await axios.get(`http://127.0.0.1:8000/products/${productId}`);
    const product = productResponse.data;
    
    // Create payload to update product
    const updatePayload = {
      name: product.name,
      description: product.description,
      price: product.price,
      stock: totalStock,
      category_id: product.category_id,
      images: product.images
    };
    
    // Update the product stock
    await axios.put(`http://127.0.0.1:8000/products/${productId}`, updatePayload);
    
    console.log(`Product ${productId} stock recalculated: ${totalStock}`);
    return totalStock;
  } catch (error) {
    console.error('Error recalculating product stock:', error);
    throw error;
  }
}

/**
 * Update variant stock after purchase
 * @param {string} variantId - ID of the variant
 * @param {number} quantity - Quantity to subtract from stock
 * @returns {Promise} - Promise that resolves when update is complete
 */
export async function updateVariantStock(variantId, quantity = 1) {
  if (!variantId) {
    console.error('No variant ID provided for stock update');
    return;
  }

  try {
    // First, get the current variant
    const response = await axios.get(`http://localhost:8000/variants/${variantId}`);
    const variant = response.data;
    
    if (!variant) {
      console.error(`Variant with ID ${variantId} not found`);
      return;
    }
    
    // Calculate new stock
    const newStock = Math.max(0, variant.stock - quantity);
    
    // Update the variant with new stock level
    await axios.patch(`http://localhost:8000/variants/${variantId}`, {
      stock: newStock
    });
    
    console.log(`Updated stock for variant ${variantId}: ${variant.stock} -> ${newStock}`);
    return newStock;
  } catch (error) {
    console.error('Error updating variant stock:', error);
    throw error;
  }
}

/**
 * Check if a product is in stock based on its variants
 * @param {Array} variants - Array of product variants
 * @returns {boolean} - True if any variant has stock > 0
 */
export function isProductInStock(variants) {
  if (!variants || variants.length === 0) return false;
  
  return variants.some(variant => variant.stock > 0);
}

/**
 * Get total available stock for a product
 * @param {Array} variants - Array of product variants
 * @returns {number} - Total stock across all variants
 */
export function getTotalProductStock(variants) {
  if (!variants || variants.length === 0) return 0;
  
  return variants.reduce((total, variant) => total + (variant.stock || 0), 0);
}

/**
 * Format stock status message
 * @param {number} stock - Stock quantity
 * @returns {object} - Formatted status with message and class
 */
export function formatStockStatus(stock) {
  if (stock <= 0) {
    return {
      message: 'สินค้าหมด',
      class: 'out-of-stock'
    };
  }
  
  if (stock <= 5) {
    return {
      message: `เหลือเพียง ${stock} ชิ้น`,
      class: 'low-stock'
    };
  }
  
  return {
    message: `มีสินค้าพร้อมส่ง`,
    class: 'in-stock'
  };
}
