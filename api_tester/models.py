# api_tester/models.py

from django.db import models
from scraping_data.models import SwaggerProject  # Importe le modèle de l'autre app


class TestResult(models.Model):
    # Lien vers le projet Swagger auquel ce test est associé
    project = models.ForeignKey(
        SwaggerProject,
        on_delete=models.CASCADE,
        related_name='test_results'
    )

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date du test")
    method = models.CharField(max_length=10)
    url = models.URLField(max_length=2000)
    status_code = models.IntegerField()
    response_body = models.TextField(blank=True, null=True)
    test_status = models.CharField(max_length=20, help_text="Ex: 'passed' ou 'failed'")

    def _str_(self):
        return f"Test {self.method} sur {self.project.name} à {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']