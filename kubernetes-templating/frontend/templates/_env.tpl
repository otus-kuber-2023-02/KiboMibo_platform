{{- define "envs" }}
{{- range $key, $value := .Values.env }}
- name: {{ $key | upper }}
  value: {{ $value | toString | quote }}
{{- end }}
{{- end }}
