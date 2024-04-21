<template>
    <div class="flex flex-col justify-center items-center">
        <p class="font-bold text-2xl pb-2">Palabras importantes</p>
        <div class="flex flex-row gap-4 bg-light-blue rounded-full text-xl font-semibold py-4 px-8 text-center min-w-96 min-h-14">
            <p v-for="word in getWords(words)" :key="word.text"
                :class="-word.Coefficient < 0 ? 'text-red' : 'text-white'">
                {{ word.word.replace(/[\.,?!]/g, '') }}: {{ -word.Coefficient.toFixed(3) }}
            </p>
        </div>
        <p class="text-sm text-gray pb-4">Las palabras importantes son aquellas que más inciden en la calificaión de una
            reseña. Los coeficientes indican su grado de importancia.</p>
    </div>
</template>
<script setup>

const {words} = defineProps({
    words: {
        type: Array,
        required: true
    }
})


const getWords = (wordList) => {
    if (!Array.isArray(wordList)) {
        return [];
    }
    wordList.sort((a, b) => a.Coefficient - b.Coefficient);
    let filtered = [...new Map(wordList.map(x => [x.word, x])).values()]
    return filtered
}
</script>