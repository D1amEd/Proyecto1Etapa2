<template>
    <div class="flex flex-row py-4 items-center justify-center">
        <div v-for="color in getStates(rating)">
            <svg :class=color class="w-36 h-36" fill="currentColor" viewBox="0 0 40 40">
                <path transform="translate(10, 8)"
                    d="M10 15.27L16.18 19l-1.64-7.03L20 8.24l-7.19-.61L10 1 7.19 7.63 0 8.24l5.46 3.73L3.82 19z" />
            </svg>
        </div>
    </div>
</template>
<script setup>
const { rating } = defineProps({
    rating: {
        type: Number,
        required: true
    }
})

const getStates = (rating) => {
    switch (rating) {
        case 0:
            return ['text-star-gray', 'text-star-gray', 'text-star-gray', 'text-star-gray', 'text-star-gray']
        case 1:
            return ['text-red', 'text-star-gray', 'text-star-gray', 'text-star-gray', 'text-star-gray']
        case 2:
            return ['text-orange', 'text-orange', 'text-star-gray', 'text-star-gray', 'text-star-gray']
        case 3:
            return ['text-yellow', 'text-yellow', 'text-yellow', 'text-star-gray', 'text-star-gray']
        case 4:
            return ['text-green', 'text-green', 'text-green', 'text-green', 'text-star-gray']
        case 5:
            return ['text-cyan', 'text-cyan', 'text-cyan', 'text-cyan', 'text-cyan']
        default:
            break;
    }
}


</script>