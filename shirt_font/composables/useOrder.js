import { ref, computed } from 'vue'
import axios from 'axios'

export default function useOrder() {
  const orders = ref([])
  const loading = ref(false)
  const error = ref(null)
  const API_URL = 'http://127.0.0.1:8000'

  // Order statistics for dashboard
  const orderStats = computed(() => {
    const total = orders.value.length
    const pending = orders.value.filter(o => o.status === 'pending').length
    const processing = orders.value.filter(o => o.status === 'processing').length
    const delivered = orders.value.filter(o => o.status === 'delivered').length
    const cancelled = orders.value.filter(o => o.status === 'cancelled').length
    
    return { total, pending, processing, delivered, cancelled }
  })

  async function fetchAllOrders() {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/orders/`)
      
      // Transform the data to match frontend expectations
      orders.value = response.data.map(order => ({
        id: order.id,
        orderNumber: `ORD-${order.id.substring(0, 6)}`,
        orderDate: order.created_at,
        status: order.status,
        paymentStatus: order.payment_status || 'unpaid',
        total: order.total_amount,
        subtotal: order.total_amount - 50, // Assuming fixed shipping fee of 50
        shippingFee: 50,
        customer: {
          name: 'Customer Name', // These would come from user data in a real app
          email: 'customer@example.com'
        },
        items: order.items.map(item => ({
          id: item.id,
          product_id: item.product_id,
          variant_id: item.variant_id,
          quantity: item.quantity,
          price: item.price,
          name: `Product ${item.product_id.substring(0, 4)}` // Placeholder
        })),
        shipping: {
          address: order.shipping_address
        },
        // Add a placeholder status history for displaying in UI
        statusHistory: [
          {
            status: order.status,
            timestamp: order.created_at,
            note: 'Order created'
          }
        ]
      }))
      
    } catch (err) {
      console.error('Error fetching orders:', err)
      error.value = err.message || 'Failed to load orders'
    } finally {
      loading.value = false
    }
  }

  async function createOrder(orderData) {
    loading.value = true
    error.value = null
    
    try {
      console.log('Creating order with data:', JSON.stringify(orderData))
      
      // Try both with and without trailing slash
      let response;
      try {
        // First try with trailing slash
        response = await axios.post(`${API_URL}/orders/`, orderData)
      } catch (err) {
        console.log('Error with trailing slash, trying without slash')
        // If that fails, try without trailing slash
        response = await axios.post(`${API_URL}/orders`, orderData)
      }
      
      console.log('Order creation response:', response)
      return response.data
    } catch (err) {
      console.error('Error creating order:', err)
      
      // Enhanced error handling
      let errorMessage = 'Failed to create order';
      
      if (err.response) {
        console.error('Response data:', err.response.data)
        console.error('Response status:', err.response.status)
        console.error('Response headers:', err.response.headers)
        
        if (err.response.status === 404) {
          errorMessage = 'API endpoint not found. Please check server configuration.';
          // Try to test the API with a simple GET request to diagnose the issue
          try {
            const testResponse = await axios.get(`${API_URL}/`)
            console.log('API root response:', testResponse.data)
          } catch (testErr) {
            console.error('Error connecting to API root:', testErr)
          }
        } else {
          errorMessage = `Error ${err.response.status}: ${err.response.data?.detail || 'Unknown error'}`;
        }
        
      } else if (err.request) {
        console.error('No response received:', err.request)
        errorMessage = 'No response received from server. Please check your connection.'
      } else {
        console.error('Error setting up request:', err.message)
        errorMessage = err.message
      }
      
      error.value = errorMessage
      throw err
    } finally {
      loading.value = false
    }
  }

  async function getOrderById(orderId) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.get(`${API_URL}/orders/${orderId}`)
      
      // Transform for frontend use
      const order = response.data
      return {
        id: order.id,
        orderNumber: `ORD-${order.id.substring(0, 6)}`,
        orderDate: order.created_at,
        status: order.status,
        paymentStatus: order.payment_status || 'unpaid',
        total: order.total_amount,
        subtotal: order.total_amount - 50,
        shippingFee: 50,
        customer: {
          name: 'Customer Name',
          email: 'customer@example.com'
        },
        items: order.items.map(item => ({
          id: item.id,
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.price,
          name: `Product ${item.product_id.substring(0, 4)}`
        })),
        shipping: {
          address: order.shipping_address
        },
        statusHistory: [
          {
            status: order.status,
            timestamp: order.created_at,
            note: 'Order created'
          }
        ]
      }
    } catch (err) {
      console.error(`Error fetching order ${orderId}:`, err)
      error.value = err.message || 'Failed to load order'
      return null
    } finally {
      loading.value = false
    }
  }

  async function updateOrderStatus(orderId, updateData) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`${API_URL}/orders/${orderId}`, updateData)
      return response.data
    } catch (err) {
      console.error(`Error updating order ${orderId}:`, err)
      error.value = err.message || 'Failed to update order'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function cancelOrder(orderId, reason) {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.put(`${API_URL}/orders/${orderId}`, {
        status: 'cancelled',
        note: reason
      })
      return response.data
    } catch (err) {
      console.error(`Error cancelling order ${orderId}:`, err)
      error.value = err.message || 'Failed to cancel order'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    orders,
    loading,
    error,
    orderStats,
    fetchAllOrders,
    createOrder,
    getOrderById,
    updateOrderStatus,
    cancelOrder
  }
}