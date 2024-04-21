<template>
    <div class="flex flex-col items-center justify-center border rounded-lg p-2 mt-4" v-if="!isLoading">
        <p class="font-bold text-xl">Subir archivo Excel para etiquetado</p>
        <p>Solo archivos formato .xlsx</p>
        <p>La columna con las reseñas a clasificar debe tener el nombre "Textos_espanol"</p>
        <input type="file" accept=".xlsx" @change="handleFileUpload" class="pt-4" />
    </div>
    <div v-else class="flex flex-col items-center justify-center border rounded-lg p-2 mt-4">
        <p>Cargando, por favor espere</p>
    </div>
</template>
<script>
import readXlsFile from 'read-excel-file'
import ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'

export default {
    data() {
        return {
            isLoading: false,
        };
    },
    methods: {
        async handleFileUpload(event) {
            this.isLoading = true;
            const file = event.target.files[0];
            const texts = []
            readXlsFile(file).then((rows) => {
                console.log(rows[0])
                if (!rows[0].includes('Textos_espanol')) {
                    alert('El archivo no es válido. Por favor, sube un archivo .xlsx donde la primera columna se llame "Textos_espanol".')
                    file = null;
                    this.isLoading = false;
                    return;
                } else {
                    rows.shift()
                    rows.forEach((row) => {
                        texts.push(row[0])
                    })
                }
            });

            if (file && file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") {
                const formData = new FormData();
                formData.append('file', file);

                const {data: preds} = await useFetch('http://localhost:8000/predict', {
                    method: 'POST',
                    body: formData
                })
                const workbook = new ExcelJS.Workbook()
                const worksheet = workbook.addWorksheet('predicciones')
                worksheet.columns = [
                    { header: 'Texto', key: 'Texto' },
                    { header: 'Puntaje', key: 'Puntaje' }
                ]
                let row = 0
                preds._rawValue.predictions.forEach((pred) => {
                    worksheet.addRow({ Texto: texts[row], Puntaje: +pred })
                    row++
                })
                const buffer = await workbook.xlsx.writeBuffer();
                const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
                saveAs(blob, 'predicciones.xlsx')
                this.isLoading = false;

            } else {
                console.log("Invalid file format. Please upload a .xlsx file.");
                this.isLoading = false;
            }
        },
    },
};
</script>