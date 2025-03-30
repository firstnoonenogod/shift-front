import { ref, computed } from 'vue'
import axios from 'axios'

export default function usePayment() {
  const payments = ref([])
  const loading = ref(false)
  const error = ref(null)
  const API_URL = 'http://127.0.0.1:8000'

  // Statistics for dashboard
  const stats = computed(() => {
    const pending = payments.value.filter(p => p.status === 'pending').length
    const approved = payments.value.filter(p => p.status === 'approved' || p.status === 'completed').length
    const rejected = payments.value.filter(p => p.status === 'rejected').length
    
    // Calculate today's total amount from approved payments
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    const todayAmount = payments.value
      .filter(p => {
        const paymentDate = new Date(p.created_at)
        return paymentDate >= today && 
              (p.status === 'approved' || p.status === 'completed')
      })
      .reduce((sum, payment) => sum + payment.amount, 0)
    
    return { pending, approved, rejected, todayAmount }
  })

  async function fetchAllPayments() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/payments/`)
      payments.value = response.data
    } catch (err) {
      console.error('Error fetching payments:', err)
      error.value = err.response?.data?.detail || err.message || 'Failed to load payments'
    } finally {
      loading.value = false
    }
  }
  
  async function getOrderPayments(orderId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/payments/order/${orderId}`)
      return response.data
    } catch (err) {
      console.error(`Error fetching payments for order ${orderId}:`, err)
      error.value = err.response?.data?.detail || err.message || 'Failed to load order payments'
      return null
    } finally {
      loading.value = false
    }
  }
  
  async function createPayment(paymentData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post(`${API_URL}/payments/`, paymentData)
      payments.value.push(response.data)
      return response.data
    } catch (err) {
      console.error('Error creating payment:', err)
      error.value = err.response?.data?.detail || err.message || 'Failed to create payment'
      throw err
    } finally {
      loading.value = false
    }
  }
  
  async function updatePaymentStatus(paymentId, updateData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`${API_URL}/payments/${paymentId}`, updateData)
      
      // Update the payment in the payments array
      const index = payments.value.findIndex(p => p.id === paymentId)
      if (index !== -1) {
        payments.value[index] = response.data
      }
      
      return response.data
    } catch (err) {
      console.error(`Error updating payment ${paymentId}:`, err)
      error.value = err.message || 'Failed to update payment'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    payments,
    loading,
    error,
    stats,
    fetchAllPayments,
    getOrderPayments,
    createPayment,
    updatePaymentStatus
  }
}
