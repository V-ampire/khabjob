/*
Миксин для работы с Vuetify формами.
Для использования в данных компонента определить параметр fields в виде объекта
fields: {
    fieldName: {
        value: '',
        errors: []
    },
    ...
}
Определяет методы:
    setInitial(initialData) - заполняет поля формы начальными данными,
      ключи initialData будут сооinitialDataтветствовать названием полей, причем поазаны будут лишь те поля
      ключи для которых присутствуют в initialData
    getAsFormData(fields) - возвращает данные формы в виде объекта FormData
    getAsObject(fields)   - возвращает данные формы в виде обычного js Object
    setErrorMessage(fieldName, errorMessage) - добавляет сообщение об ошибке для поля fieldName
*/

export default {
    data () {
      return {
        fields: null,
        initialData: null
      }
    },
    methods: {
        getAsFormData (fields=[]) {
          const formData = new FormData();
          const formFields = this.cleanFields(this._getFormFields(fields));
          for (let field in formFields) {
            formData.append(field, formFields[field]);
          }
          return formData
        },
        getAsObject (fields=[]) {
          return this.cleanFields(this._getFormFields(fields));
        },
        setErrorMessages (fieldName, errorMessages=[]) {
          /**
           * @errorMessages - массив ошибок
           */
          this.fields[fieldName].errors = errorMessages;
        },
        setInitial (initialData) {
          /**
           * Устанавливает в свойство this.fields.value начальные данные
           * @initialFields - начальный данные
           */
          this.initialData = initialData;
          if (this.initialData) {
            for (let key in initialData) {
              if (key in this.fields) {
                this.fields[key].value = initialData[key]
              }
            }  
          }
        },
        validate () {
          return this.$refs.form.validate();
        },
        reset () {
          return this.$refs.form.reset();
        },
        cleanFields(formFields) {
          /**
           * Переопределив этот метод можно изменить, либо проверить поля перед тем,
           * как из них будут получены значения для методов getAsFormData и getAsObject.
           * Метод должен возвращать объект содержащий пары ключ-значение,
           * где ключи - это названия полей формы,
           * а значения - необходимые значения полей формы
           */
          return formFields
        },
        _getFormFields(fields=[]) {
          /**
           * Возвращает объект содержащий пары ключ-значение,
           * где ключи - это ключи из объекта field,
           * а значения - значения fields.field.value
           * @fields - поля которые должны быть в форме
           */
          let result = {};
          const useFields = (fields.length > 0) ? fields : Object.keys(this.fields);
          for (let field of useFields) {
            result[field] = this.fields[field].value;
          }
          return result
        }
    }
}