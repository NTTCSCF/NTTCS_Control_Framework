import mimetypes
from time import sleep, time
from typing import Dict, Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView

import json
import pandas as pd

from acounts.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime

from ..models import Assessment, MaturirtyTable, AsociacionMarcos, Assessmentguardados, \
    NttcsCf20231, Domains, Evidencerequestcatalog, Evidencias, MapeoMarcos, AssessmentCreados, \
    AsociacionEvidenciasGenericas, AsociacionEvidenciasCreadas, TiposIniciativas, Iniciativas, \
    AssessmentEs, MaturirtyTableEs, EvidencerequestcatalogEs, Cliente, Proyecto, AsociacionUsuariosProyecto, \
    AsociacionProyectoAssessment, ProyectosMejora, AsociacionProyectoMejoraIniciativa, Entrevistas, \
    AsociacionEntrevistasUsuarios, AsociacionPlanProyectosProyectos, PlanProyectoMejora, DependenciaProyecto

from django.views.generic import TemplateView, ListView
import mysql.connector
from django.contrib import messages
import csv
from bs4 import BeautifulSoup

from docx import Document
from docx.shared import Cm