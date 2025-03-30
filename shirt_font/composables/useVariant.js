import { ref } from 'vue'
import axios from 'axios'

export default function useVariant() {
  const variants = ref([])
  const variant = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const API_URL = 'http://127.0.0.1:8000'

  const fetchAllVariants = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/variants/`)
      console.log('Variants response:', response.data)
      variants.value = response.data
      return response.data
    } catch (err) {
      console.error('Error fetching variants:', err)
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch variants'
      return []
    } finally {
      loading.value = false
    }
  }

  const fetchProductVariants = async (productId) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/variants/product/${productId}`)
      console.log(`Variants for product ${productId}:`, response.data)
      variants.value = response.data
      return response.data
    } catch (err) {
      console.error(`Error fetching variants for product ${productId}:`, err)
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch product variants'
      return []
    } finally {
      loading.value = false
    }
  }

  const fetchVariant = async (variantId) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/variants/${variantId}`)
      variant.value = response.data
      return response.data
    } catch (err) {
      console.error(`Error fetching variant ${variantId}:`, err)
      error.value = err.response?.data?.detail || err.message || 'Failed to fetch variant'
      return null
    } finally {
      loading.value = false
    }
  }

  const createVariant = async (variantData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post(`${API_URL}/variants/`, variantData)
      variants.value.push(response.data)
      return response.data
    } catch (err) {
      console.error('Error creating variant:', err)
      error.value = err.response?.data?.detail || err.message || 'Failed to create variant'
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateVariant = async (variantId, variantData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`${API_URL}/variants/${variantId}`, variantData)
      
      // Update the variant in the variants array
      const index = variants.value.findIndex(v => v.id === variantId)
      if (index !== -1) {
        variants.value[index] = response.data
      }
      
      return response.data
    } catch (err) {
      console.error(`Error updating variant ${variantId}:`, err)
      error.value = err.response?.data?.detail || err.message || 'Failed to update variant'
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteVariant = async (variantId) => {
    loading.value = true
    error.value = null
    
    try {
      await axios.delete(`${API_URL}/variants/${variantId}`)
      
      // Remove the variant from the variants array
      variants.value = variants.value.filter(v => v.id !== variantId)
      
      return true
    } catch (err) {
      console.error(`Error deleting variant ${variantId}:`, err)
      error.value = err.response?.data?.detail || err.message || 'Failed to delete variant'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    variants,
    variant,
    loading,
    error,
    fetchAllVariants,
    fetchProductVariants,
    fetchVariant,
    createVariant,
    updateVariant,
    deleteVariant
  }
}
