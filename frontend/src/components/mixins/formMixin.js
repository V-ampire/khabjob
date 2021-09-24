/**
 * Mixin for components with form.
 * Provide methods to get fields values as FormData oj Object.
 * All Date fields converts to string in ISO format.
 */

import { convertToISODateString } from '@/utils.js'

export default {
  data() {
    return {
      fields: null,
    }
  },
  methods: {
    getAsFormData() {
      const formData = new FormData()
        for (let field in this.fields) {
          const value = this.cleanField(this.fields[field].value)
          if (value !== null && value !== undefined) {
            formData.append(field, value)
          }
        }
      return formData
    },
    getAsObject() {
      let result = {}
      for (let field of Object.keys(this.fields)) {
        const value = this.cleanField(this.fields[field].value)
        if (value !== null && value !== undefined) {
          result[field] = value
        }
      }
      return result
    },
    resetFields() {
      for (let field in this.fields) {
        this.fields[field].value = null
        this.fields[field].error = null
      }
    },
    cleanField(fieldValue) {
      if (fieldValue instanceof Date) {
        return convertToISODateString(fieldValue)
      }
      return fieldValue
    },
    setInitial (initialData) {
      for (let key in initialData) {
        if (key in this.fields) {
          this.fields[key].value = initialData[key]
        }
      }  
    },
    setError(fieldName, errorMessage) {
      this.fields[fieldName].error = errorMessage
    }
  },
}