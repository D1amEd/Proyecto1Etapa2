<template>
  <div class="w-screen h-screen flex flex-col font-inter bg-light-gray">
<div class="flex flex-row bg-dark-blue">
  <div class="flex flex-col px-20 pb-6 pt-3 font-semibold gap-1">
      <p class="text-light-blue text-lg">Turismo de los Alpes</p>
      <p class="text-white text-2xl">Evaluador de Reseñas</p>
    </div>
    <div class="flex flex-col justify-center">
      <div @click="show = !show" class="hover:cursor-pointer rounded-full bg-light-blue text-white font-semibold py-2 px-4">Métricas</div>
      <div v-if="show" class="flex flex-col bg-light-blue rounded-lg p-2 mt-4 items-center justify-center self-center">
        <p class="font-semibold text-xl">Mátriz de confución de prueba</p>
        <img src="~/assets/matrix.jpg" alt="confusion matrix" class="w-2/3 py-2"></img>
        <p class="text-xl font-semibold">Métricas del modelo</p>
        <img src="~/assets/stats.jpg" alt="stats" class="w-1/3 py-2"></img>

      </div>
    </div>
</div>
    <div class="flex flex-col px-32">
      <div class="flex flex-col pt-10">
        <p class="font-bold text-xl pb-5">Ingresa una reseña</p>
        <textarea class="w-full h-32 border-2 border-gray-500 rounded-lg p-2" v-model="review" placeholder="Escribe aquí..."></textarea>
      </div>  
    </div>
    <div class="flex flex-col px-32 pt-10 items-center">
      <button class="bg-yellow text-lg font-semibold rounded-lg p-2 w-30 text-center" @click="handlePrompt">Predecir puntaje</button>
      <Stars :rating="score"></Stars>
      <Words :words="words"></Words>
      <button class="bg-yellow text-lg font-semibold rounded-lg p-2 w-30 text-center" @click="clear">Nueva reseña</button>
      <FileLoader></FileLoader>
    </div>

  </div>
  <div>

  </div>
</template>
<script>
import { ref } from 'vue'
import Stars from './components/stars.vue';
import Words from './components/words.vue';
import FileLoader from './components/fileLoader.vue';
import ExcelJS from 'exceljs'

export default {
  components:{
    Stars,
    Words,
    FileLoader
  },
  setup() {
    const review = ref('')
    const score = ref(0)
    const words = ref([])
    const show = ref(false)

    const clear = () => {
      words.value = []
      review.value = ''
      score.value = 0
    }

    const handlePrompt = async () => {
      const rows = [ review.value ]

      const workbook = new ExcelJS.Workbook()
      const worksheet = workbook.addWorksheet('predicciones')
      worksheet.columns = [
        { header: 'Textos_espanol', key: 'Texto' },
      ]
      rows.forEach((row) => {
        worksheet.addRow({ Texto: row })
      })

      const buffer = await workbook.xlsx.writeBuffer();
      const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })

      const formData = new FormData()
      formData.append('file', new File([blob], "file.xlsx"))

      fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        score.value = data.predictions[0]
        words.value = data.palabras[0]
      })
    }
    
    return {
      review,
      score,
      words,
      clear,
      handlePrompt,
      show
    }
  }
}
</script>
