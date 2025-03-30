import axios from 'axios';

// Interface with ID
interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  category_id: string;
  images: string[];
}

// Interface without ID for creating products
interface CreateProductInput {
  name: string;
  description: string;
  price: number;
  stock: number;
  category_id: string;
  images: string[];
}

// Function to get all products
export async function getProduct(): Promise<Product[]> {
  try {
    const response = await axios.get('http://127.0.0.1:8000/products/');
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    throw error;
  }
}

// Function to create a new product
export async function createProduct(productData: CreateProductInput): Promise<Product> {
  try {
    const response = await axios.post('http://127.0.0.1:8000/products/', productData);
    return response.data;
  } catch (error) {
    console.error('Error creating product:', error);
    throw error;
  }
}

// Function to get a product by ID
export async function getProductById(id: string): Promise<Product> {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/products/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching product with ID ${id}:`, error);
    throw error;
  }
}

// Function to update a product by ID
export async function updateProduct(id: string, productData: CreateProductInput): Promise<Product> {
  try {
    const response = await axios.put(`http://127.0.0.1:8000/products/${id}`, productData);
    return response.data;
  } catch (error) {
    console.error(`Error updating product with ID ${id}:`, error);
    throw error;
  }
}

// Function to delete a product by ID
export async function deleteProduct(id: string): Promise<void> {
  try {
    await axios.delete(`http://127.0.0.1:8000/products/${id}`);
  } catch (error) {
    console.error(`Error deleting product with ID ${id}:`, error);
    throw error;
  }
}
