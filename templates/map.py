{% extends "base.html" %}

{% block title %}Mapa - WebGIS Kevin{% endblock %}

{% block extra_css %}
<style>
    /* Prevenir overflow global */
    body, html {
        overflow-x: hidden;
        overflow-y: hidden;
        max-width: 100vw;
    }
    
    #map-container {
        height: calc(100vh - 140px);
        position: relative;
        overflow: hidden;
    }
    
    #map {
        height: 100%;
        width: 100%;
    }
    
    .sidebar {
        position: absolute;
        top: 10px;
        left: 10px;
        z-index: 1000;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-width: 300px;
        min-width: 250px;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .sidebar-header {
        background: #0d6efd;
        color: white;
        padding: 15px;
        border-radius: 8px 8px 0 0;
    }
    
    .sidebar-body {
        padding: 15px;
    }
    
    .tool-button {
        width: 100%;
        margin-bottom: 8px;
        text-align: left;
    }
    
    .coordinates-display {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.9em;
        margin-top: 10px;
    }
    
    .layer-info {
        background: #e9ecef;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-size: 0.9em;
    }
    
    @media (max-width: 768px) {
        .sidebar {
            max-width: 100%;
            min-width: auto;
            left: 5px;
            right: 5px;
        }
        
        /* Ajustar elementos fixos em telas pequenas */
        .position-fixed {
            max-width: calc(100vw - 20px);
            left: 10px !important;
            right: 10px !important;
        }
    }

    .sidebar.minimized {
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
        overflow: hidden;
        padding: 0;
        transition: width 0.2s;
    }
    .sidebar.minimized .sidebar-header {
        justify-content: center !important;
    }
    .sidebar.minimized .sidebar-title {
        display: flex !important;
        color: #fff !important;
        font-weight: bold;
        font-size: 1.1rem;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 12px 0;
    }
    .sidebar.minimized .sidebar-body {
        display: none;
    }
</style>
{% endblock %}

{% block content %}
<div id="map-container">
    <div id="map"></div>
    
    <!-- Botão/Janela de Zoom recolhível no canto direito -->
    <div class="position-fixed" style="top: 24px; right: 32px; z-index: 2000; width: 260px;">
        <div class="card shadow border-0" style="border-radius: 2rem;">
            <div class="card-header d-flex justify-content-between align-items-center p-2" style="background:#ff9038; color:#fff; border-radius: 2rem;">
                <span class="fw-bold"><i class="fas fa-expand-arrows-alt me-2"></i> Zoom para</span>
                <button class="btn btn-sm btn-light" id="toggle-zoom-panel" title="Expandir painel"><i id="zoom-chevron" class="fas fa-chevron-down"></i></button>
            </div>
            <div class="collapse" id="zoom-panel-body">
                <button class="btn btn-outline-primary w-100 fw-bold py-2" id="zoom-leste-fluminense" style="border-radius:1.5rem; margin: 12px 0;">
                    Leste Fluminense
                </button>
            </div>
        </div>
    </div>

    <!-- Legenda de Cores -->
    <div class="position-fixed" style="bottom: 28px; right: 55px; z-index: 1000;">
        <div class="card shadow border-0" style="border-radius: 1rem; background: rgba(255,255,255,0.95);">
            <div class="card-header p-2" style="background:#005eb8; color:#fff; border-radius: 1rem;">
                <span class="fw-bold"><i class="fas fa-palette me-2"></i>Legenda</span>
            </div>
            <div class="card-body p-2">
                <div class="d-flex align-items-center mb-1">
                    <div style="width: 12px; height: 12px; background: #28a745; border-radius: 50%; margin-right: 8px;"></div>
                    <small>Municipal</small>
                </div>
                <div class="d-flex align-items-center mb-1">
                    <div style="width: 12px; height: 12px; background: #007bff; border-radius: 50%; margin-right: 8px;"></div>
                    <small>Estadual</small>
                </div>
                <div class="d-flex align-items-center mb-1">
                    <div style="width: 12px; height: 12px; background: #dc3545; border-radius: 50%; margin-right: 8px;"></div>
                    <small>Federal</small>
                </div>
                <div class="d-flex align-items-center mb-1">
                    <div style="width: 12px; height: 12px; background: #ffc107; border-radius: 50%; margin-right: 8px;"></div>
                    <small>Privada</small>
                </div>
                <div class="d-flex align-items-center">
                    <div style="width: 12px; height: 12px; background: #6c757d; border-radius: 50%; margin-right: 8px;"></div>
                    <small>Não informado</small>
                </div>
            </div>
        </div>
    </div>

    <!-- Painel de Estatísticas do Município -->
    <div class="position-fixed" style="top: 24px; right: 320px; z-index: 2000; width: 300px; display: none; max-height: 80vh; overflow-y: auto;" id="stats-panel">
        <div class="card shadow border-0" style="border-radius: 2rem;">
            <div class="card-header d-flex justify-content-between align-items-center p-2" style="background:#005eb8; color:#fff; border-radius: 2rem;">
                <span class="fw-bold"><i class="fas fa-chart-bar me-2"></i> <span id="stats-municipio-nome">Município</span></span>
                <button class="btn btn-sm btn-light" id="close-stats-panel" title="Fechar painel"><i class="fas fa-times"></i></button>
            </div>
            <div class="card-body p-3">
                <div class="mb-3">
                    <h6 class="text-primary fw-bold mb-2">
                        <i class="fas fa-school me-2"></i>Resumo Geral
                    </h6>
                    <div class="row text-center">
                        <div class="col-6">
                            <div class="bg-primary text-white rounded p-2 mb-2" style="color: white !important;">
                                <strong id="stats-total-escolas">0</strong>
                                <br><small>Total de Escolas</small>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="bg-success text-white rounded p-2 mb-2">
                                <strong id="stats-escolas-publicas">0</strong>
                                <br><small>Públicas</small>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mb-3">
                    <h6 class="text-primary fw-bold mb-2">
                        <i class="fas fa-building me-2"></i>Por Dependência
                    </h6>
                    <div id="stats-dependencia" class="small">
                        <!-- Dados serão inseridos aqui -->
                    </div>
                </div>

                <div class="mb-3">
                    <h6 class="text-primary fw-bold mb-2">
                        <i class="fas fa-graduation-cap me-2"></i>Por Etapas de Ensino
                    </h6>
                    <div id="stats-etapas" class="small">
                        <!-- Dados serão inseridos aqui -->
                    </div>
                </div>

                <div class="mb-3">
                    <h6 class="text-primary fw-bold mb-2">
                        <i class="fas fa-users me-2"></i>Por Porte
                    </h6>
                    <div id="stats-porte" class="small">
                        <!-- Dados serão inseridos aqui -->
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Sidebar com ferramentas -->
    <div class="sidebar minimized" id="sidebar" style="top: 24px;">
        <div class="sidebar-header d-flex justify-content-between align-items-center" style="justify-content: center !important;">
            <span class="sidebar-title text-white d-flex align-items-center" style="white-space:nowrap;">
                <i class="fas fa-desktop me-2" style="color:#ff9038;"></i>
                Central de Comando
            </span>
            <button id="toggle-sidebar" class="btn btn-sm btn-light ms-2" title="Expandir barra de ferramentas">
                <i id="sidebar-chevron" class="fas fa-chevron-down"></i>
            </button>
        </div>
        <div class="sidebar-body">
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="text-muted mb-2">
                        <i class="fas fa-layer-group me-1"></i>
                        Mapas Base
                    </h6>
                    <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-base-maps" aria-expanded="false" aria-controls="collapse-base-maps">
                        <i id="chevron-base-maps" class="fas fa-chevron-down"></i>
                    </button>
                </div>
                <div class="collapse" id="collapse-base-maps">
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="baseMap" id="cartodb" value="cartodb" checked>
                        <label class="form-check-label" for="cartodb">
                            CartoDB Positron
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="baseMap" id="google" value="google">
                        <label class="form-check-label" for="google">
                            Google Satellite
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="baseMap" id="osm" value="osm">
                        <label class="form-check-label" for="osm">
                            OpenStreetMap
                        </label>
                    </div>
                </div>
            </div>
            
            <hr>
            
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="text-muted mb-2">
                        <i class="fas fa-map" style="transform: rotate(-15deg);"></i>
                        Dados cartográficos
                    </h6>
                    <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-dados-cartograficos" aria-expanded="false" aria-controls="collapse-dados-cartograficos">
                        <i id="chevron-dados-cartograficos" class="fas fa-chevron-down"></i>
                    </button>
                </div>
                <div class="collapse" id="collapse-dados-cartograficos">
                    <div class="coordinates-display mb-2">
                        <strong>Coordenadas:</strong><br>
                        <span id="coordinates">Clique no mapa</span>
                    </div>
                    <div class="layer-info">
                        <strong>Informações:</strong><br>
                        <small>Zoom: <span id="zoom-level">5</span></small><br>
                        <small>Escala: <span id="scale">~1:10,000,000</span></small>
                    </div>
                </div>
            </div>

            <hr>

            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="text-muted mb-2">
                        <i class="fas fa-city me-1"></i>
                        Municípios
                    </h6>
                    <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-municipios" aria-expanded="false" aria-controls="collapse-municipios">
                        <i id="chevron-municipios" class="fas fa-chevron-down"></i>
                    </button>
                </div>
                <div class="collapse" id="collapse-municipios">
                    <div class="mb-2 ms-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="fw-bold" style="color:#ff9038;"><i class="fas fa-map me-1"></i> Leste Fluminense</span>
                            <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-leste-flu" aria-expanded="false" aria-controls="collapse-leste-flu">
                                <i id="chevron-leste-flu" class="fas fa-chevron-down"></i>
                            </button>
                        </div>
                        <div class="collapse show" id="collapse-leste-flu">
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="Todos" id="municipio-todos" checked>
                                <label class="form-check-label" for="municipio-todos">Todos</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="Niterói" id="municipio-niteroi">
                                <label class="form-check-label" for="municipio-niteroi">Niterói</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="São Gonçalo" id="municipio-sao-goncalo">
                                <label class="form-check-label" for="municipio-sao-goncalo">São Gonçalo</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="Maricá" id="municipio-marica">
                                <label class="form-check-label" for="municipio-marica">Maricá</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="Itaboraí" id="municipio-itaborai">
                                <label class="form-check-label" for="municipio-itaborai">Itaboraí</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="Tanguá" id="municipio-tangua">
                                <label class="form-check-label" for="municipio-tangua">Tanguá</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input municipio-checkbox" type="checkbox" value="Rio Bonito" id="municipio-rio-bonito">
                                <label class="form-check-label" for="municipio-rio-bonito">Rio Bonito</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <hr>

            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="text-muted mb-2">
                        <i class="fas fa-filter me-1"></i>
                        Filtro por Tipo
                    </h6>
                    <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-tipos" aria-expanded="false" aria-controls="collapse-tipos">
                        <i id="chevron-tipos" class="fas fa-chevron-down"></i>
                    </button>
                </div>
                <div class="collapse" id="collapse-tipos">
                    <div class="mb-2 ms-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="fw-bold" style="color:#ff9038;"><i class="fas fa-building me-1"></i> Por Dependência</span>
                            <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-dependencias" aria-expanded="false" aria-controls="collapse-dependencias">
                                <i id="chevron-dependencias" class="fas fa-chevron-down"></i>
                            </button>
                        </div>
                        <div class="collapse show" id="collapse-dependencias">
                            <div class="form-check">
                                <input class="form-check-input tipo-checkbox" type="checkbox" value="Todos" id="tipo-todos" checked>
                                <label class="form-check-label" for="tipo-todos">Todos os Tipos</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input tipo-checkbox" type="checkbox" value="Municipal" id="tipo-municipal">
                                <label class="form-check-label" for="tipo-municipal">Municipal</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input tipo-checkbox" type="checkbox" value="Estadual" id="tipo-estadual">
                                <label class="form-check-label" for="tipo-estadual">Estadual</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input tipo-checkbox" type="checkbox" value="Federal" id="tipo-federal">
                                <label class="form-check-label" for="tipo-federal">Federal</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input tipo-checkbox" type="checkbox" value="Privada" id="tipo-privada">
                                <label class="form-check-label" for="tipo-privada">Privada</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <hr>
            
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <h6 class="text-muted mb-2">
                        <i class="fas fa-fire me-1"></i>
                        Heatmaps
                    </h6>
                    <button class="btn btn-sm btn-outline-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse-heatmaps" aria-expanded="false" aria-controls="collapse-heatmaps">
                        <i id="chevron-heatmaps" class="fas fa-chevron-down"></i>
                    </button>
                </div>
                <div class="collapse" id="collapse-heatmaps">
                    <div class="form-check">
                        <input class="form-check-input heatmap-checkbox" type="checkbox" value="geral" id="heatmap-geral">
                        <label class="form-check-label" for="heatmap-geral">Geral</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input heatmap-checkbox" type="checkbox" value="municipio" id="heatmap-municipio">
                        <label class="form-check-label" for="heatmap-municipio">Por Município</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input heatmap-checkbox" type="checkbox" value="tipo" id="heatmap-tipo">
                        <label class="form-check-label" for="heatmap-tipo">Por Tipo</label>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
// Variáveis globais
let map;
let currentBaseMap = 'cartodb';

// Variável global para camada de escolas
let escolasLayer;
let municipiosLayer;

// Variáveis para heatmaps
let heatmapLayer = null;
let heatmapData = [];
let currentHeatmapType = null;
let currentHeatmapValue = null;

// Inicializar mapa
function initMap() {
    // Criar mapa base
    map = L.map('map', {
        center: [-15.7801, -47.9292],
        zoom: 5,
        zoomControl: false // Desativa o controle padrão
    });
    
    // Definir mapas base
    const baseMaps = {
        cartodb: L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors © <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 19
        }),
        google: L.tileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
            attribution: '© Google Satellite',
            maxZoom: 20
        }),
        osm: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 19
        })
    };
    
    // Adicionar mapa base inicial
    baseMaps.cartodb.addTo(map);

    // Adiciona o controle de zoom no canto inferior direito
    L.control.zoom({ position: 'bottomright' }).addTo(map);
    
    // Event listeners para mudança de mapa base
    document.querySelectorAll('input[name="baseMap"]').forEach(radio => {
        radio.addEventListener('change', function() {
            const selectedMap = this.value;
            map.removeLayer(baseMaps[currentBaseMap]);
            baseMaps[selectedMap].addTo(map);
            currentBaseMap = selectedMap;
        });
    });
    
    // Event listeners para coordenadas
    map.on('mousemove', function(e) {
        const lat = e.latlng.lat.toFixed(6);
        const lng = e.latlng.lng.toFixed(6);
        document.getElementById('coordinates').textContent = `${lat}, ${lng}`;
    });
    
    // Event listeners para zoom
    map.on('zoomend', function() {
        const zoom = map.getZoom();
        document.getElementById('zoom-level').textContent = zoom;
        
        // Calcular escala aproximada
        const scale = Math.round(591657550.5 / Math.pow(2, zoom));
        document.getElementById('scale').textContent = `~1:${scale.toLocaleString()}`;
    });
    
    // Carregar dados de exemplo
}

// Função para carregar dados de exemplo

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', initMap);

// Sidebar toggle
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggle-sidebar');
let sidebarMinimized = true;

function updateSidebarChevron() {
    if (sidebarMinimized) {
        document.getElementById('sidebar-chevron').className = 'fas fa-chevron-down';
    } else {
        document.getElementById('sidebar-chevron').className = 'fas fa-chevron-up';
    }
}

// Função para atualizar chevrons das seções da Central de Comando
function updateSectionChevron(sectionId) {
    const collapseEl = document.getElementById(sectionId);
    const chevron = document.getElementById('chevron-' + sectionId.replace('collapse-', ''));
    if (collapseEl && chevron) {
        if (collapseEl.classList.contains('show')) {
            chevron.className = 'fas fa-chevron-up';
        } else {
            chevron.className = 'fas fa-chevron-down';
        }
    }
}

// Ao expandir a sidebar, manter todas as seções recolhidas
function collapseAllSections() {
    const sections = [
        'collapse-base-maps',
        'collapse-dados-cartograficos',
        'collapse-heatmaps'
    ];
    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el && el.classList.contains('show')) {
            new bootstrap.Collapse(el, {toggle: false}).hide();
        }
    });
}

// Inicializa o estado correto da seta
updateSidebarChevron();

toggleBtn.addEventListener('click', function() {
    sidebarMinimized = !sidebarMinimized;
    if (sidebarMinimized) {
        sidebar.classList.add('minimized');
        toggleBtn.title = 'Expandir barra de ferramentas';
    } else {
        sidebar.classList.remove('minimized');
        toggleBtn.title = 'Minimizar barra de ferramentas';
        collapseAllSections();
    }
    updateSidebarChevron();
});

// Inicializa chevrons
['collapse-base-maps','collapse-dados-cartograficos','collapse-municipios','collapse-leste-flu','collapse-heatmaps'].forEach(function(id) {
    updateSectionChevron(id);
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener('shown.bs.collapse', function() { updateSectionChevron(id); });
        el.addEventListener('hidden.bs.collapse', function() { updateSectionChevron(id); });
    }
});

// Zoom para painel recolhível
const zoomPanelBody = document.getElementById('zoom-panel-body');
const zoomPanelChevron = document.getElementById('zoom-chevron');
// Inicia recolhido
if (zoomPanelBody.classList.contains('show')) {
    new bootstrap.Collapse(zoomPanelBody, {toggle: false}).hide();
    zoomPanelChevron.className = 'fas fa-chevron-down';
}
document.getElementById('toggle-zoom-panel').addEventListener('click', function() {
    if (zoomPanelBody.classList.contains('show')) {
        new bootstrap.Collapse(zoomPanelBody, {toggle: false}).hide();
        zoomPanelChevron.className = 'fas fa-chevron-down';
    } else {
        new bootstrap.Collapse(zoomPanelBody, {toggle: false}).show();
        zoomPanelChevron.className = 'fas fa-chevron-up';
    }
});

// Botão de zoom para Leste Fluminense (usa a extensão dos dados atuais)
document.getElementById('zoom-leste-fluminense').addEventListener('click', function() {
    if (municipiosLayer) {
        map.fitBounds(municipiosLayer.getBounds());
        setTimeout(function() {
            map.setZoom(map.getZoom() + 1);
        }, 400); // Pequeno delay para garantir que o fitBounds termine
    }
});

// Lógica de filtro de escolas por município
let escolasGeoJsonData = null;
let escolasLayerGroup = null;
let municipiosGeoJsonData = null;
let municipiosHighlightLayer = null;

// Funções para heatmaps
function onHeatmapCheckboxChange(e) {
    const heatmapType = e.target.value;
    const isChecked = e.target.checked;
    
    if (isChecked) {
        // Desmarcar outros heatmaps
        document.querySelectorAll('.heatmap-checkbox').forEach(cb => {
            if (cb.value !== heatmapType) {
                cb.checked = false;
            }
        });
        
        // Criar heatmap
        criarHeatmap(heatmapType);
    } else {
        // Remover heatmap
        removerHeatmap();
    }
}

function criarHeatmap(tipo) {
    if (!escolasGeoJsonData) return;
    
    // Remover heatmap anterior
    removerHeatmap();
    
    // Preparar dados para heatmap
    let dadosHeatmap = [];
    
    if (tipo === 'geral') {
        // Heatmap geral de todas as escolas
        escolasGeoJsonData.features.forEach(feature => {
            if (feature.geometry && feature.geometry.coordinates) {
                dadosHeatmap.push([
                    feature.geometry.coordinates[1],
                    feature.geometry.coordinates[0],
                    1
                ]);
            }
        });
    } else if (tipo === 'municipio') {
        // Heatmap por município (usar município selecionado)
        const municipioSelecionado = Array.from(document.querySelectorAll('.municipio-checkbox:checked')).find(cb => cb.value !== 'Todos');
        if (municipioSelecionado) {
            const municipio = municipioSelecionado.value;
            escolasGeoJsonData.features.forEach(feature => {
                const municipioEscola = feature.properties.Município || feature.properties.MUNICIPIO || feature.properties.municipio || feature.properties.NM_MUNICIPIO;
                if (municipioEscola === municipio && feature.geometry && feature.geometry.coordinates) {
                    dadosHeatmap.push([
                        feature.geometry.coordinates[1],
                        feature.geometry.coordinates[0],
                        1
                    ]);
                }
            });
        }
    } else if (tipo === 'tipo') {
        // Heatmap por tipo (usar tipo selecionado)
        const tipoSelecionado = Array.from(document.querySelectorAll('.tipo-checkbox:checked')).find(cb => cb.value !== 'Todos');
        if (tipoSelecionado) {
            const tipo = tipoSelecionado.value;
            escolasGeoJsonData.features.forEach(feature => {
                const dependencia = feature.properties.Dependênc || feature.properties.DEPENDENCIA || feature.properties.dependencia || 'Não informado';
                if (dependencia === tipo && feature.geometry && feature.geometry.coordinates) {
                    dadosHeatmap.push([
                        feature.geometry.coordinates[1],
                        feature.geometry.coordinates[0],
                        1
                    ]);
                }
            });
        }
    }
    
    if (dadosHeatmap.length > 0) {
        heatmapData = dadosHeatmap;
        currentHeatmapType = tipo;
        
        // Criar heatmap usando Leaflet.heat
        heatmapLayer = L.heatLayer(dadosHeatmap, {
            radius: 40,
            blur: 40,
            maxZoom: 15,
            gradient: {0.0: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1: 'red'}
        }).addTo(map);
    }
}

function removerHeatmap() {
    if (heatmapLayer) {
        map.removeLayer(heatmapLayer);
        heatmapLayer = null;
        heatmapData = [];
        currentHeatmapType = null;
        currentHeatmapValue = null;
    }
}

function atualizarEscolasFiltradas() {
    if (!escolasGeoJsonData) return;
    
    // Remover camadas anteriores
    if (escolasLayerGroup) {
        map.removeLayer(escolasLayerGroup);
    }
    if (municipiosHighlightLayer) {
        map.removeLayer(municipiosHighlightLayer);
    }
    
    // Obter municípios e tipos selecionados
    const selecionados = Array.from(document.querySelectorAll('.municipio-checkbox:checked')).map(cb => cb.value);
    const tiposSelecionados = Array.from(document.querySelectorAll('.tipo-checkbox:checked')).map(cb => cb.value);
    
    // Filtrar escolas por município e tipo
    let featuresFiltradas = escolasGeoJsonData.features;
    
    // Aplicar filtros apenas se não estiver "Todos" selecionado
    if (!selecionados.includes('Todos') || !tiposSelecionados.includes('Todos')) {
        featuresFiltradas = escolasGeoJsonData.features.filter(f => {
            const municipio = f.properties.Município || f.properties.MUNICIPIO || f.properties.municipio || f.properties.NM_MUNICIPIO;
            const dependencia = f.properties.Dependênc || f.properties.DEPENDENCIA || f.properties.dependencia || 'Não informado';
            
            // Filtro por município
            const municipioValido = selecionados.includes('Todos') || selecionados.includes(municipio);
            
            // Filtro por tipo
            const tipoValido = tiposSelecionados.includes('Todos') || tiposSelecionados.includes(dependencia);
            
            return municipioValido && tipoValido;
        });
    }
    
    // Destacar municípios selecionados
    if (municipiosGeoJsonData && !selecionados.includes('Todos')) {
        const municipiosSelecionados = municipiosGeoJsonData.features.filter(f => {
            const municipio = f.properties.NM_MUNICIPIO || f.properties.Município || f.properties.MUNICIPIO || f.properties.municipio;
            return selecionados.includes(municipio);
        });
        
        municipiosHighlightLayer = L.geoJSON({type: 'FeatureCollection', features: municipiosSelecionados}, {
            style: { 
                color: '#ff9038', 
                weight: 3, 
                fillOpacity: 0.2,
                fillColor: '#ff9038'
            }
        }).addTo(map);
    }
    
    // Adicionar escolas filtradas
    escolasLayerGroup = L.geoJSON({type: 'FeatureCollection', features: featuresFiltradas}, {
        pointToLayer: function(feature, latlng) {
            // Definir cor baseada no tipo de dependência
            let color = '#005eb8'; // Azul padrão
            const dependencia = feature.properties.Dependênc || feature.properties.DEPENDENCIA || feature.properties.dependencia || 'Não informado';
            
            switch(dependencia) {
                case 'Municipal':
                    color = '#28a745'; // Verde
                    break;
                case 'Estadual':
                    color = '#007bff'; // Azul
                    break;
                case 'Federal':
                    color = '#dc3545'; // Vermelho
                    break;
                case 'Privada':
                    color = '#ffc107'; // Amarelo
                    break;
                default:
                    color = '#6c757d'; // Cinza para não informado
            }
            
            return L.circleMarker(latlng, {
                radius: 6,
                fillColor: color,
                color: color,
                weight: 2,
                opacity: 1,
                fillOpacity: 0.8
            });
        },
        onEachFeature: function (feature, layer) {
            if (feature.properties) {
                const nome = feature.properties.Escola || feature.properties.NOME_ESC || feature.properties.NOME || 'Escola';
                const municipio = feature.properties.Município || feature.properties.MUNICIPIO || feature.properties.municipio || feature.properties.NM_MUNICIPIO || 'N/A';
                const endereco = feature.properties.Endereço || feature.properties.ENDERECO || feature.properties.ADDRESS || 'N/A';
                const dependencia = feature.properties.Dependênc || feature.properties.DEPENDENCIA || feature.properties.dependencia || 'Não informado';
                
                // Definir cor do tipo de dependência
                let dependenciaColor = '#6c757d'; // Cinza padrão
                switch(dependencia) {
                    case 'Municipal':
                        dependenciaColor = '#28a745';
                        break;
                    case 'Estadual':
                        dependenciaColor = '#007bff';
                        break;
                    case 'Federal':
                        dependenciaColor = '#dc3545';
                        break;
                    case 'Privada':
                        dependenciaColor = '#ffc107';
                        break;
                }
                
                layer.bindPopup(`
                    <div style="min-width: 200px;">
                        <strong style="color: #005eb8;">${nome}</strong><br>
                        <small><strong>Município:</strong> ${municipio}</small><br>
                        <small><strong>Dependência:</strong> <span style="color: ${dependenciaColor}; font-weight: bold;">${dependencia}</span></small><br>
                        <small><strong>Endereço:</strong> ${endereco}</small>
                    </div>
                `);
            }
        }
    }).addTo(map);
    
    // Ajustar zoom se houver escolas filtradas (apenas quando há filtros aplicados)
    if (featuresFiltradas.length > 0 && !selecionados.includes('Todos')) {
        map.fitBounds(escolasLayerGroup.getBounds());
    }
}

// Carregar dados dos municípios
fetch('/data/mun_leste_flu_2')
    .then(response => response.json())
    .then(data => {
        municipiosGeoJsonData = data;
        municipiosLayer = L.geoJSON(data, {
            style: { 
                color: '#ff9038', 
                weight: 1, 
                fillOpacity: 0.05,
                fillColor: '#ff9038'
            }
        }).addTo(map);
        
        // Zoom inicial para o Leste Fluminense
        map.fitBounds(municipiosLayer.getBounds());
        setTimeout(function() {
            map.setZoom(map.getZoom() + 1);
        }, 400);
    })
    .catch(error => console.error('Erro ao carregar camada de municípios:', error));

// Carregar camada GeoJSON das escolas
fetch('/data/escolas_possiveis_rj_inep')
    .then(response => response.json())
    .then(data => {
        escolasGeoJsonData = data;
        atualizarEscolasFiltradas();
    })
    .catch(error => console.error('Erro ao carregar camada de escolas:', error));

// Função para calcular estatísticas do município
function calcularEstatisticasMunicipio(municipio) {
    if (!escolasGeoJsonData) return;
    
    const escolasMunicipio = escolasGeoJsonData.features.filter(f => 
        f.properties.Município === municipio
    );
    
    if (escolasMunicipio.length === 0) return;
    
    // Estatísticas gerais
    const totalEscolas = escolasMunicipio.length;
    const escolasPublicas = escolasMunicipio.filter(e => 
        e.properties.Categoria === 'Pública'
    ).length;
    
    // Por dependência
    const dependencias = {};
    escolasMunicipio.forEach(escola => {
        const dep = escola.properties.Dependênc || 'Não informado';
        dependencias[dep] = (dependencias[dep] || 0) + 1;
    });
    
    // Por etapas de ensino
    const etapas = {};
    escolasMunicipio.forEach(escola => {
        const etapasEscola = escola.properties['Etapas e M'] || 'Não informado';
        if (etapasEscola && etapasEscola !== 'Não informado') {
            etapasEscola.split(', ').forEach(etapa => {
                const etapaTrim = etapa.trim();
                if (etapaTrim) {
                    etapas[etapaTrim] = (etapas[etapaTrim] || 0) + 1;
                }
            });
        }
    });
    
    // Por porte
    const portes = {};
    escolasMunicipio.forEach(escola => {
        const porte = escola.properties['Porte da E'] || 'Não informado';
        portes[porte] = (portes[porte] || 0) + 1;
    });
    
    return {
        totalEscolas,
        escolasPublicas,
        dependencias,
        etapas,
        portes
    };
}

// Função para exibir estatísticas no painel
function exibirEstatisticasMunicipio(municipio) {
    const stats = calcularEstatisticasMunicipio(municipio);
    if (!stats) return;
    
    // Atualizar título
    document.getElementById('stats-municipio-nome').textContent = municipio;
    
    // Atualizar resumo geral
    document.getElementById('stats-total-escolas').textContent = stats.totalEscolas;
    document.getElementById('stats-escolas-publicas').textContent = stats.escolasPublicas;
    
    // Atualizar dependências
    let dependenciaHtml = '';
    Object.entries(stats.dependencias).forEach(([dep, count]) => {
        dependenciaHtml += `<div class="d-flex justify-content-between mb-1">
            <span>${dep}</span>
            <span class="badge bg-primary text-white" style="color: white !important;">${count}</span>
        </div>`;
    });
    document.getElementById('stats-dependencia').innerHTML = dependenciaHtml;
    
    // Atualizar etapas
    let etapasHtml = '';
    Object.entries(stats.etapas).forEach(([etapa, count]) => {
        etapasHtml += `<div class="d-flex justify-content-between mb-1">
            <span>${etapa}</span>
            <span class="badge bg-success text-white">${count}</span>
        </div>`;
    });
    document.getElementById('stats-etapas').innerHTML = etapasHtml;
    
    // Atualizar portes
    let portesHtml = '';
    Object.entries(stats.portes).forEach(([porte, count]) => {
        portesHtml += `<div class="d-flex justify-content-between mb-1">
            <span>${porte}</span>
            <span class="badge bg-warning text-dark">${count}</span>
        </div>`;
    });
    document.getElementById('stats-porte').innerHTML = portesHtml;
    
    // Mostrar painel
    document.getElementById('stats-panel').style.display = 'block';
}

// Event listeners para checkboxes
function onMunicipioCheckboxChange(e) {
    if (e.target.value === 'Todos') {
        // Se marcar "Todos", desmarca os outros
        if (e.target.checked) {
            document.querySelectorAll('.municipio-checkbox').forEach(cb => {
                if (cb.value !== 'Todos') cb.checked = false;
            });
        }
        // Esconder painel de estatísticas
        document.getElementById('stats-panel').style.display = 'none';
    } else {
        // Se marcar qualquer outro, desmarca "Todos"
        if (e.target.checked) {
            document.getElementById('municipio-todos').checked = false;
            // Mostrar estatísticas do município selecionado
            exibirEstatisticasMunicipio(e.target.value);
        } else {
            // Se desmarcou, verificar se ainda há algum selecionado
            const algumMarcado = Array.from(document.querySelectorAll('.municipio-checkbox')).some(cb => cb.value !== 'Todos' && cb.checked);
            if (!algumMarcado) {
                document.getElementById('municipio-todos').checked = true;
                document.getElementById('stats-panel').style.display = 'none';
            }
        }
    }
    atualizarEscolasFiltradas();
}

function onTipoCheckboxChange(e) {
    if (e.target.value === 'Todos') {
        // Se marcar "Todos", desmarca os outros
        if (e.target.checked) {
            document.querySelectorAll('.tipo-checkbox').forEach(cb => {
                if (cb.value !== 'Todos') cb.checked = false;
            });
        }
    } else {
        // Se marcar qualquer outro, desmarca "Todos"
        if (e.target.checked) {
            document.getElementById('tipo-todos').checked = false;
        } else {
            // Se desmarcou, verificar se ainda há algum selecionado
            const algumMarcado = Array.from(document.querySelectorAll('.tipo-checkbox')).some(cb => cb.value !== 'Todos' && cb.checked);
            if (!algumMarcado) {
                document.getElementById('tipo-todos').checked = true;
            }
        }
    }
    atualizarEscolasFiltradas();
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.municipio-checkbox').forEach(cb => {
        cb.addEventListener('change', onMunicipioCheckboxChange);
    });
    
    document.querySelectorAll('.tipo-checkbox').forEach(cb => {
        cb.addEventListener('change', onTipoCheckboxChange);
    });
    
    document.querySelectorAll('.heatmap-checkbox').forEach(cb => {
        cb.addEventListener('change', onHeatmapCheckboxChange);
    });
    
    // Event listener para fechar painel de estatísticas
    document.getElementById('close-stats-panel').addEventListener('click', function() {
        document.getElementById('stats-panel').style.display = 'none';
    });
});
</script>
{% endblock %} 