import axios from 'axios';

// Interface for order items
interface OrderItem {
    product_id: string;
    variant_id: string;
    quantity: number;
}

// Interface with ID for complete order
interface Order {
    id: string;
    items: OrderItem[];
    shipping_address: string;
    status?: string;
    created_at?: string;
}

// Interface without ID for creating orders
interface OrderInput {
    items: OrderItem[];
    shipping_address: string;
}

// Get all orders
export async function getAllOrders(): Promise<Order[]> {
    try {
        const response = await axios.get('http://127.0.0.1:8000/orders/');
        return response.data;
    } catch (error) {
        console.error('Error fetching all orders:', error);
        throw error;
    }
}

// Get orders by user ID
export async function getOrdersByUserId(userId: string): Promise<Order[]> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/orders/${userId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching orders for user ID ${userId}:`, error);
        throw error;
    }
}

// Get order by ID
export async function getOrderById(orderId: string): Promise<Order> {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/orders/${orderId}`);
        return response.data;
    } catch (error) {
        console.error(`Error fetching order ID ${orderId}:`, error);
        throw error;
    }
}

// Create new order
export async function createOrder(orderData: OrderInput): Promise<Order> {
    try {
        const response = await axios.post('http://127.0.0.1:8000/orders/', orderData);
        return response.data;
    } catch (error) {
        console.error('Error creating order:', error);
        throw error;
    }
}

// Update order
export async function updateOrder(orderId: string, orderData: OrderInput): Promise<Order> {
    try {
        const response = await axios.put(`http://127.0.0.1:8000/orders/${orderId}`, orderData);
        return response.data;
    } catch (error) {
        console.error(`Error updating order ID ${orderId}:`, error);
        throw error;
    }
}

// Delete order
export async function deleteOrder(orderId: string): Promise<void> {
    try {
        await axios.delete(`http://127.0.0.1:8000/orders/${orderId}`);
    } catch (error) {
        console.error(`Error deleting order ID ${orderId}:`, error);
        throw error;
    }
}