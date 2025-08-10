from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import time
import random
import logging
from threading import Thread, Event, Lock
import requests
from your_ip_pool_module import CommercialIPPool
from urllib.parse import urljoin

# Configuración centralizada de logging
logger = logging.getLogger(__name__)

@dataclass
class ViewerStats:
    total_requests: int = 0
    successful: int = 0
    failed: int = 0
    bandwidth: int = 0  # in bytes
    
    def reset(self):
        for field in self.__annotations__:
            setattr(self, field, 0)

# User agents 
class RealisticUserAgents:
    def __init__(self):
        # Fuente actualizada de user agents reales
        self.desktop_agents = self._load_user_agents("desktop")
        self.mobile_agents = self._load_user_agents("mobile")
        self.tablet_agents = self._load_user_agents("tablet")
        
        # Distribución realista de dispositivos
        self.device_distribution = {
            'desktop': 0.65,
            'mobile': 0.30,
            'tablet': 0.05
        }
    
    def _load_user_agents(self, device_type: str) -> List[str]:
        """Carga user agents desde un archivo o API"""
        try:
            with open(f"user_agents_{device_type}.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            # Lista de respaldo actualizada (2023)
            return self._get_default_agents(device_type)
    
    def _get_default_agents(self, device_type: str) -> List[str]:
        """User agents actualizados por categoría"""
        agents = {
            'desktop': [
                # Windows
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                # Mac
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
            ],
            'mobile': [
                # Android
                "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
                # iPhone
                "Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1",
            ],
            'tablet': [
                "Mozilla/5.0 (iPad; CPU OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 13; SM-T870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            ]
        }
        return agents.get(device_type, [])
    
    def get_random_user_agent(self) -> str:
        """Devuelve un user agent siguiendo distribución real de dispositivos"""
        device = random.choices(
            list(self.device_distribution.keys()),
            weights=list(self.device_distribution.values()),
            k=1
        )[0]
        
        agents = getattr(self, f"{device}_agents")
        return random.choice(agents)

 # Patrones de navegacion

    class HumanLikeBehavior:
    def __init__(self):
        # Tiempos de reacción humanos reales (en segundos)
        self.action_delays = {
            'page_load': (1.5, 3.8),
            'between_clicks': (0.8, 2.5),
            'reading_time': (3.0, 12.0),
            'scrolling': (0.5, 1.8)
        }
        
        # Patrones de navegación típicos
        self.browsing_patterns = [
            {'actions': ['load', 'scroll', 'pause', 'scroll', 'click', 'pause']},
            {'actions': ['load', 'pause', 'scroll', 'pause', 'scroll', 'pause']},
            {'actions': ['load', 'click', 'pause', 'scroll', 'click', 'pause']}
        ]
    
    def simulate_human_delay(self, action_type: str):
        """Simula tiempos de espera humanos realistas"""
        if action_type in self.action_delays:
            min_d, max_d = self.action_delays[action_type]
            time.sleep(random.uniform(min_d, max_d))
    
    def generate_mouse_movement(self, width: int, height: int) -> List[Tuple[int, int]]:
        """Genera coordenadas de movimiento de mouse humano"""
        points = []
        x, y = random.randint(0, width), random.randint(0, height)
        
        for _ in range(random.randint(3, 8)):
            dx = random.randint(-50, 50)
            dy = random.randint(-30, 30)
            x = max(0, min(width, x + dx))
            y = max(0, min(height, y + dy))
            points.append((x, y))
            time.sleep(random.uniform(0.05, 0.3))
        
        return points
    
    def get_browsing_pattern(self):
        """Devuelve un patrón de navegación aleatorio pero realista"""
        pattern = random.choice(self.browsing_patterns)
        return pattern['actions']

 # Simulacion de mensaje en el chat

 class ChatSimulator:
    def __init__(self, channel: str):
        self.channel = channel
        self.chat_url = f"https://kick.com/api/v2/channels/{channel}/messages"
        self.common_messages = self._load_chat_messages()
        self.user_profiles = self._generate_user_profiles(100)
        
    def _load_chat_messages(self) -> List[str]:
        """Carga mensajes típicos de chat desde archivo"""
        try:
            with open("chat_messages.txt", "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]
        except:
            return [
                "¡Buen stream!",
                "LUL",
                "Kappa",
                "GG",
                "F",
                "PogChamp",
                "Hola a todos!",
                "El stream se ve genial hoy",
                "¿Jugarás más tarde?",
                "¡Buena jugada!"
            ]
    
    def _generate_user_profiles(self, count: int) -> List[Dict]:
        """Genera perfiles de usuario realistas"""
        profiles = []
        for i in range(count):
            profiles.append({
                'username': f"user_{random.randint(1000, 9999)}",
                'message_frequency': random.uniform(0.1, 1.5),  # mensajes por minuto
                'message_style': random.choice(['casual', 'spammy', 'emotive', 'questioner']),
                'emote_probability': random.uniform(0.1, 0.7)
            })
        return profiles
    
    def simulate_chat_activity(self, viewer_count: int):
        """Simula actividad de chat realista basada en cantidad de viewers"""
        active_chatters = max(1, int(viewer_count * 0.15))  # 15% de viewers activos en chat
        
        for _ in range(active_chatters):
            Thread(
                target=self._chat_worker,
                daemon=True
            ).start()
    
    def _chat_worker(self):
        """Hilo independiente que simula un usuario de chat"""
        profile = random.choice(self.user_profiles)
        session = requests.Session()
        
        while True:
            try:
                # Espera según frecuencia del perfil
                delay = 60 / profile['message_frequency']
                time.sleep(delay * random.uniform(0.7, 1.3))
                
                # Genera mensaje según estilo
                message = self._generate_message(profile)
                
                # Envía mensaje al chat (simulado)
                self._send_chat_message(session, message, profile['username'])
                
            except Exception as e:
                logger.error(f"Error en chat worker: {str(e)}")
                time.sleep(5)
    
    def _generate_message(self, profile: Dict) -> str:
        """Genera un mensaje de chat realista según perfil"""
        if random.random() < profile['emote_probability']:
            return random.choice(self.common_messages)
        
        # Mensajes más personalizados según estilo
        if profile['message_style'] == 'questioner':
            return random.choice([
                f"¿{random.choice(['Cómo', 'Dónde', 'Por qué'])} {random.choice(['hiciste', 'conseguiste', 'lograste'])} eso?",
                "¿Alguien más tiene este problema?",
                "¿Qué juego es este?"
            ])
        elif profile['message_style'] == 'emotive':
            return random.choice([
                f"¡{random.choice(['Increíble', 'Asombroso', 'Genial'])}!",
                "NO PUEDO CREERLO OMG",
                "Esto es épico!!!!"
            ])
        else:
            return random.choice(self.common_messages)
    
    def _send_chat_message(self, session: requests.Session, message: str, username: str):
        """Envía un mensaje al chat (simulación)"""
        # En una implementación real necesitarías manejar autenticación
        headers = {
            "User-Agent": RealisticUserAgents().get_random_user_agent(),
            "Content-Type": "application/json"
        }
        
        payload = {
            "content": message,
            "username": username
        }
        
        # Esto es solo una simulación - no envía realmente el mensaje
        logger.debug(f"CHAT SIMULATION: {username}: {message}")
        
        # En producción necesitarías:
        # session.post(self.chat_url, json=payload, headers=headers)

 # Tester
 
class KickStreamTester:
    def __init__(self, pool: CommercialIPPool, channel: str, max_viewers: int = 5):
        # ... (código existente)
        
        # Mejoras de realismo
        self.user_agent_manager = RealisticUserAgents()
        self.behavior_simulator = HumanLikeBehavior()
        self.chat_simulator = ChatSimulator(channel)
        
        # Configuración de realismo
        self.enable_chat_simulation = True
        self.enable_human_browsing = True
    
    def _simulate_viewer(self, viewer_id: int):
        """Versión mejorada con comportamiento realista"""
        try:
            # Comportamiento humano inicial
            if self.enable_human_browsing:
                self._simulate_initial_browsing(viewer_id)
            
            # Actividad principal
            while not self.stop_event.is_set():
                # ... (código existente de visualización)
                
                # Interacción con chat
                if self.enable_chat_simulation and random.random() < 0.15:
                    self._simulate_chat_interaction(viewer_id)
                
                # Pausas humanas entre acciones
                self.behavior_simulator.simulate_human_delay('between_actions')
        
        except Exception as e:
            logger.error(f"Viewer {viewer_id} error: {str(e)}")
    
    def _simulate_initial_browsing(self, viewer_id: int):
        """Simula navegación inicial humana"""
        pattern = self.behavior_simulator.get_browsing_pattern()
        
        for action in pattern:
            if action == 'load':
                self.behavior_simulator.simulate_human_delay('page_load')
            elif action == 'pause':
                self.behavior_simulator.simulate_human_delay('reading_time')
            elif action == 'scroll':
                self._simulate_scrolling(viewer_id)
    
    def _simulate_chat_interaction(self, viewer_id: int):
        """Simula interacción con el chat"""
        username = f"viewer_{viewer_id}_{random.randint(100,999)}"
        message = self.chat_simulator._generate_message(
            random.choice(self.chat_simulator.user_profiles)
        )
        
        logger.debug(f"Viewer {viewer_id} sending chat message as {username}: {message}")
        # self.chat_simulator._send_chat_message(session, message, username)
        
        # Tiempo de lectura de respuesta
        self.behavior_simulator.simulate_human_delay('reading_time')


 # Métodos

     def _validate_channel(self):
        """Verifica que el canal exista antes de empezar"""
        try:
            resp = requests.get(self.api_url, timeout=10)
            if resp.status_code != 200:
                raise ValueError(f"Canal '{self.channel}' no encontrado")
        except Exception as e:
            logger.error(f"Error validando canal: {str(e)}")
            raise

    def _update_stats(self, success: bool, bandwidth: int = 0):
        """Actualiza estadísticas de forma thread-safe"""
        with self.stats_lock:
            self.stats.total_requests += 1
            if success:
                self.stats.successful += 1
                self.stats.bandwidth += bandwidth
            else:
                self.stats.failed += 1

    def _get_headers(self) -> Dict[str, str]:
        """Genera headers con rotación de User-Agent"""
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": self.base_url,
            "Referer": self.web_url,
            "Connection": "keep-alive"
        }

    def _create_session(self, proxy: str) -> requests.Session:
        """Crea una sesión con configuración común"""
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        session.headers.update(self._get_headers())
        return session

 # Simulación

     def _simulate_viewer(self, viewer_id: int):
        """Simula el comportamiento de un viewer real con mejor manejo de errores"""
        session = None
        last_success = time.time()
        
        while not self.stop_event.is_set():
            try:
                proxy = self.pool.get_ip()
                if not proxy:
                    logger.warning(f"Viewer {viewer_id} - No hay IPs disponibles")
                    time.sleep(5)
                    continue
                
                session = self._create_session(proxy)
                
                # Comportamiento humano con tiempo aleatorio
                time.sleep(random.uniform(self.min_sleep, self.max_sleep))
                
                # 1. Visita la página web
                if not self._visit_webpage(session, viewer_id):
                    continue
                
                # 2. Descarga playlist HLS
                segments = self._download_hls_playlist(session, viewer_id)
                if not segments:
                    continue
                
                # 3. Descarga segmentos de video
                self._download_video_segments(session, segments, viewer_id)
                
                logger.info(f"Viewer {viewer_id} - Simulación exitosa | IP: {proxy.split('@')[-1]}")
                last_success = time.time()
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Viewer {viewer_id} - Error de conexión: {str(e)}")
                self._update_stats(False)
                self._handle_viewer_error(viewer_id, last_success)
            except Exception as e:
                logger.error(f"Viewer {viewer_id} - Error inesperado: {str(e)}", exc_info=True)
                self._update_stats(False)
                self._handle_viewer_error(viewer_id, last_success)
            finally:
                if session:
                    session.close()

    def enhance_viewbot_simulation(self):
    # 1. Patrones de visualización variables
    self.viewing_patterns = [
        {'min_time': 30, 'max_time': 120, 'min_segments': 3, 'max_segments': 8},
        {'min_time': 60, 'max_time': 300, 'min_segments': 5, 'max_segments': 10},
        {'min_time': 10, 'max_time': 60, 'min_segments': 2, 'max_segments': 5}
    ]
    
    # 2. Comportamiento de "viewer fantasma" (reconexiones)
    self.ghost_viewer_probability = 0.2  # 20% de chance de desconexión/reconexión
    
    # 3. Delay aleatorio entre acciones
    self.random_actions = [
        {'name': 'chat_message', 'probability': 0.1},
        {'name': 'page_refresh', 'probability': 0.05},
        {'name': 'quality_change', 'probability': 0.07}
    ]

 # Métodos auxiliares

     def _visit_webpage(self, session: requests.Session, viewer_id: int) -> bool:
        """Visita la página web del canal"""
        try:
            resp = session.get(self.web_url, timeout=self.session_timeout)
            self._update_stats(resp.status_code == 200)
            
            if resp.status_code != 200:
                logger.warning(f"Viewer {viewer_id} - Fallo página web: {resp.status_code}")
                return False
            return True
        except Exception as e:
            logger.warning(f"Viewer {viewer_id} - Error página web: {str(e)}")
            self._update_stats(False)
            return False

    def _download_hls_playlist(self, session: requests.Session, viewer_id: int) -> List[str]:
        """Descarga y parsea la playlist HLS"""
        try:
            headers = {**self._get_headers(), "Accept": "application/vnd.apple.mpegurl"}
            resp = session.get(self.hls_url, headers=headers, timeout=self.session_timeout)
            self._update_stats(resp.status_code == 200)
            
            if resp.status_code != 200:
                logger.warning(f"Viewer {viewer_id} - Fallo playlist HLS: {resp.status_code}")
                return []
            
            return self._parse_hls_playlist(resp.text)
        except Exception as e:
            logger.warning(f"Viewer {viewer_id} - Error playlist HLS: {str(e)}")
            self._update_stats(False)
            return []

    def _download_video_segments(self, session: requests.Session, segments: List[str], viewer_id: int):
        """Descarga segmentos de video de forma aleatoria"""
        base_url = self.hls_url.rsplit('/', 1)[0]
        segments_to_download = random.sample(segments, k=min(random.randint(2, 4), len(segments)))
        
        for seg in segments_to_download:
            try:
                seg_url = urljoin(f"{base_url}/", seg)
                with session.get(seg_url, timeout=self.session_timeout, stream=True) as resp:
                    content_length = int(resp.headers.get('content-length', 0))
                    self._update_stats(resp.status_code == 200, content_length)
                    
                    if resp.status_code == 200:
                        # Simular tiempo de visualización
                        time.sleep(random.uniform(2.0, 6.0))
                    else:
                        logger.warning(f"Viewer {viewer_id} - Error segmento: {resp.status_code}")
            except Exception as e:
                logger.warning(f"Viewer {viewer_id} - Error descargando segmento: {str(e)}")
                self._update_stats(False)


 # Manejo de threads

     def start(self):
        """Inicia los viewers simulados con manejo mejorado de threads"""
        if self.viewers:
            logger.warning("Los viewers ya están en ejecución")
            return

        logger.info(f"Iniciando {self.max_viewers} viewers para {self.channel}")
        
        try:
            for i in range(self.max_viewers):
                viewer_thread = Thread(
                    target=self._simulate_viewer,
                    args=(i+1,),
                    daemon=True,
                    name=f"KickViewer-{i+1}"
                )
                viewer_thread.start()
                self.viewers.append(viewer_thread)
            
            # Hilo para estadísticas
            Thread(
                target=self._show_stats,
                daemon=True,
                name="StatsMonitor"
            ).start()
        except Exception as e:
            logger.error(f"Error al iniciar viewers: {str(e)}")
            self.stop()
            raise

    def stop(self):
        """Detiene todos los viewers de forma segura"""
        if not self.stop_event.is_set():
            self.stop_event.set()
            logger.info("Deteniendo todos los viewers...")
            
            # Esperar a que terminen los threads
            for viewer in self.viewers:
                if viewer.is_alive():
                    viewer.join(timeout=5)
            
            self.viewers.clear()
            self.stop_event.clear()
            logger.info("Todos los viewers han sido detenidos")

 # Mejoras adicionales

     def _handle_viewer_error(self, viewer_id: int, last_success: float):
        """Maneja errores y decide si reintentar o esperar"""
        error_delay = 5  # segundos base
        time_since_success = time.time() - last_success
        
        # Aumentar delay si hay muchos errores consecutivos
        if time_since_success > 30:
            error_delay = min(30, error_delay + (time_since_success // 10))
        
        time.sleep(error_delay)

    def _show_stats(self):
        """Muestra estadísticas periódicamente con formato mejorado"""
        while not self.stop_event.is_set():
            with self.stats_lock:
                stats = f"""
                Estadísticas:
                - Total requests: {self.stats.total_requests}
                - Exitosas: {self.stats.successful} ({self._get_success_rate()}%)
                - Fallidas: {self.stats.failed}
                - Tráfico: {self.stats.bandwidth / (1024*1024):.2f} MB
                - Viewers activos: {sum(1 for t in self.viewers if t.is_alive())}/{self.max_viewers}
                """
                logger.info(stats)
            time.sleep(10)

    def _get_success_rate(self) -> float:
        """Calcula el porcentaje de éxito"""
        if self.stats.total_requests == 0:
            return 0.0
        return round((self.stats.successful / self.stats.total_requests) * 100, 2)

    def get_current_stats(self) -> ViewerStats:
        """Devuelve una copia de las estadísticas actuales"""
        with self.stats_lock:
            return ViewerStats(
                total_requests=self.stats.total_requests,
                successful=self.stats.successful,
                failed=self.stats.failed,
                bandwidth=self.stats.bandwidth
            )
    
 # Sistema de autoverificación

    def self_test(self):
    """Ejecuta pruebas automáticas para verificar que todo funciona"""
    tests = {
        'proxy_pool': self._test_proxy_pool(),
        'stream_access': self._test_stream_access(),
        'viewer_simulation': self._test_viewer_simulation(),
        'request_headers': self._test_request_headers()
    }
    
    if all(tests.values()):
        logger.info("✅ Todas las pruebas pasaron correctamente")
        return True
    else:
        for test, result in tests.items():
            if not result:
                logger.error(f"❌ Falló la prueba: {test}")
        return False

def _test_proxy_pool(self):
    try:
        proxy = self.pool.get_ip()
        if not proxy:
            return False
            
        session = requests.Session()
        session.proxies = {"http": proxy, "https": proxy}
        response = session.get("https://httpbin.org/ip", timeout=10)
        return response.status_code == 200
    except:
        return False


 # Simulacion de ABR (calidad del stream)

    def simulate_quality_switching(self, session: requests.Session, viewer_id: int):
    """Simula cambios de calidad como haría un viewer real"""
    qualities = ["160p", "360p", "480p", "720p", "1080p"]
    current_quality = random.choice(qualities)
    
    # 20% de probabilidad de cambiar de calidad
    if random.random() < 0.2:
        new_quality = random.choice([q for q in qualities if q != current_quality])
        logger.debug(f"Viewer {viewer_id} cambiando de {current_quality} a {new_quality}")
        current_quality = new_quality
    
    # Modificar URL para la calidad seleccionada
    return self.hls_url.replace("master.m3u8", f"{current_quality}.m3u8")

 # Camuflaje

    def apply_anti_detection_measures(self):
    """Técnicas para reducir la probabilidad de detección"""
    self.protection_features = {
        'random_delays': True,  # Entre 1-5 segundos aleatorios entre requests
        'human_mouse_movement': False,  # Requeriría integración con browser automation
        'natural_viewing_patterns': True,
        'realistic_quality_switches': True,
        'variable_session_times': True,  # No todos los viewers ven el mismo tiempo
        'realistic_start_times': True  # Los viewers no se conectan todos al mismo tiempo
    }
    
    # Configuración de delays aleatorios
    self.min_delay = 0.5  # segundos
    self.max_delay = 3.0  # segundos
    
    # Variabilidad en tiempo de sesión
    self.min_session_time = 120  # 2 minutos
    self.max_session_time = 1800  # 30 minutos

 # Implementacion
    
    def run_full_test(self, test_duration: int = 3600):
    """Ejecuta una prueba completa de viewbotting"""
    if not self.is_stream_live():
        logger.error("El canal no está en vivo. Iniciando stream de prueba...")
        stream_manager = TestStreamManager()
        if not stream_manager.start_test_stream():
            logger.error("No se pudo iniciar el stream de prueba")
            return False
        
        logger.info("Stream de prueba iniciado. Esperando 30 segundos...")
        time.sleep(30)
    
    if not self.self_test():
        logger.error("No se pueden iniciar los viewers debido a fallos en las pruebas")
        return False
    
    logger.info("Iniciando simulación de viewbotting...")
    self.start()
    
    start_time = time.time()
    while (time.time() - start_time) < test_duration and not self.stop_event.is_set():
        time.sleep(10)
        self.save_stats_to_file()
    
    self.stop()
    logger.info("Prueba completada")
    
    if 'stream_manager' in locals():
        stream_manager.stop_test_stream()
    
    return True