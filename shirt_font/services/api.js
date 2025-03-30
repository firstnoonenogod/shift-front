import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

// Create axios instance with base URL and default headers
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Payment API
export const paymentApi = {
  // Get all payments (admin)
  getAllPayments: () => api.get('/payments/all'),
  
  // Get payments by user
  getUserPayments: (userId) => api.get(`/payments/user/${userId}`),
  
  // Get payments by order
  getOrderPayments: (orderId) => api.get(`/payments/order/${orderId}`),
  
  // Get payment by ID
  getPaymentById: (paymentId) => api.get(`/payments/${paymentId}`),
  
  // Create new payment
  createPayment: (paymentData) => api.post('/payments/', paymentData),
  
  // Update payment status
  updatePaymentStatus: (paymentId, updateData) => api.put(`/payments/${paymentId}`, updateData),
  
  // Delete payment
  deletePayment: (paymentId) => api.delete(`/payments/${paymentId}`)
};

// Order API
export const orderApi = {
  // Get all orders
  getAllOrders: () => api.get('/orders'),
  
  // Get order by ID
  getOrderById: (orderId) => api.get(`/orders/${orderId}`),
  
  // Get orders by user
  getUserOrders: (userId) => api.get(`/orders/user/${userId}`),
  
  // Create new order
  createOrder: (orderData) => api.post('/orders', orderData),
  
  // Update order status
  updateOrderStatus: (orderId, statusData) => api.put(`/orders/${orderId}/status`, statusData),
  
  // Cancel order
  cancelOrder: (orderId, reason) => api.put(`/orders/${orderId}/cancel`, { reason })
};

// Add request interceptor for authentication if needed
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
