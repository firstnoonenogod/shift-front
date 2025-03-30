import axios from 'axios';

// Interface with ID for complete payment
interface Payment {
    id: string;
    order_id: string;
    amount: number;
    payment_method: string;
    status: 'pending' | 'completed' | 'failed';
    created_at?: string;
}

// Interface without ID for creating payments
interface PaymentInput {
    order_id: string;
    amount: number;
    payment_method: string;
    status: 'pending' | 'completed' | 'failed';
}

// Get all payments
export async function getAllPayments(): Promise<Payment[]> {
    try {
        const response = await axios.get('http://127.0.0.1:8000/payments/all');
        return response.data;
    } catch (error) {
        console.error('Error fetching all payments:', error);
        throw error;
    }
}

// Get payments list
export async function getPayments(): Promise<Payment[]> {
    try {
        const response = await axios.get('http://127.0.0.1:8000/payments/');
        return response.data;
    } catch (error) {
        console.error('Error fetching payments:', error);
        throw error;
    }
}

// Get payments by order ID
export async function getPaymentsByOrderId(orderId: string): Promise<Payment[]> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/payments/order/${orderId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching payments for order ID ${orderId}:`, error);
        throw error;
    }
}

// Get payments by user ID
export async function getPaymentsByUserId(userId: string): Promise<Payment[]> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/payments/user/${userId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching payments for user ID ${userId}:`, error);
        throw error;
    }
}

// Get payment by ID
export async function getPaymentById(paymentId: string): Promise<Payment> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/payments/${paymentId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching payment ID ${paymentId}:`, error);
        throw error;
    }
}

// Create new payment
export async function createPayment(paymentData: PaymentInput): Promise<Payment> {
    try {
        const response = await axios.post('http://127.0.0.1:8000/payments/', paymentData);
        return response.data;
    } catch (error) {
        console.error('Error creating payment:', error);
        throw error;
    }
}

// Update payment
export async function updatePayment(paymentId: string, paymentData: PaymentInput): Promise<Payment> {
    try {
        const response = await axios.put(`http://127.0.0.1:8000/payments/${paymentId}`, paymentData);
        return response.data;
    } catch (error) {
        console.error(`Error updating payment ID ${paymentId}:`, error);
        throw error;
    }
}

// Delete payment
export async function deletePayment(paymentId: string): Promise<void> {
    try {
        await axios.delete(`http://127.0.0.1:8000/payments/${paymentId}`);
    } catch (error) {
        console.error(`Error deleting payment ID ${paymentId}:`, error);
        throw error;
    }
}