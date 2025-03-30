<template>
    <div class="modal-overlay" v-if="show" @click.self="close">
        <div class="modal-container">
            <div class="modal-header">
                <h3>เพิ่มลงตะกร้าสำเร็จ</h3>
                <button class="close-button" @click="close">×</button>
            </div>

            <div class="modal-content">
                <div class="item-details">
                    <div class="item-image">
                        <img :src="item.image" :alt="item.name" />
                    </div>
                    <div class="item-info">
                        <div class="item-name">{{ item.name }}</div>
                        <div class="item-options">
                            <span v-if="item.size">ขนาด: {{ item.size }}</span>
                            <span v-if="item.color">สี: {{ item.color }}</span>
                        </div>
                        <div class="item-quantity">จำนวน: {{ item.quantity }}</div>
                        <div class="item-price">฿{{ item.price }}</div>
                    </div>
                </div>
            </div>

            <div class="modal-actions">
                <button class="continue-shopping" @click="close">เลือกซื้อสินค้าต่อ</button>
                <button class="view-cart" @click="viewCart">ดูตะกร้าสินค้า</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CartConfirmation',
    props: {
        show: {
            type: Boolean,
            default: false
        },
        item: {
            type: Object,
            default: () => ({})
        }
    },
    methods: {
        close() {
            this.$emit('close');
        },
        viewCart() {
            this.$router.push('/cart');
            this.close();
        }
    }
};
</script>

<style scoped>
.modal-overlay
{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-container
{
    background-color: white;
    border-radius: 8px;
    width: 90%;
    max-width: 450px;
    max-height: 90vh;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    animation: slide-up 0.3s;
}

@keyframes slide-up
{
    from
    {
        transform: translateY(30px);
        opacity: 0;
    }

    to
    {
        transform: translateY(0);
        opacity: 1;
    }
}

.modal-header
{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #f0f0f0;
}

.modal-header h3
{
    margin: 0;
    color: #333;
    font-size: 18px;
}

.close-button
{
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #999;
}

.modal-content
{
    padding: 20px;
}

.item-details
{
    display: flex;
    gap: 15px;
}

.item-image
{
    width: 80px;
    height: 80px;
    border: 1px solid #f0f0f0;
    border-radius: 4px;
    overflow: hidden;
}

.item-image img
{
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.item-info
{
    flex: 1;
}

.item-name
{
    font-weight: 600;
    margin-bottom: 8px;
}

.item-options
{
    display: flex;
    gap: 15px;
    font-size: 14px;
    color: #666;
    margin-bottom: 4px;
}

.item-quantity
{
    font-size: 14px;
    color: #666;
}

.item-price
{
    font-weight: 600;
    color: #ee4d2d;
    margin-top: 8px;
}

.modal-actions
{
    display: flex;
    padding: 15px 20px;
    gap: 10px;
    border-top: 1px solid #f0f0f0;
}

.continue-shopping,
.view-cart
{
    flex: 1;
    padding: 10px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.continue-shopping
{
    background-color: white;
    border: 1px solid #ddd;
    color: #333;
}

.continue-shopping:hover
{
    border-color: #ccc;
    background-color: #f9f9f9;
}

.view-cart
{
    background-color: #ee4d2d;
    border: 1px solid #ee4d2d;
    color: white;
}

.view-cart:hover
{
    background-color: #d73211;
}
</style>
