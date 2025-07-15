document.addEventListener('DOMContentLoaded', function() {
    // --- CONSTANTS & CONFIGURATION ---
    const COMMAND_CENTER_COORDS = [13.064, 80.180]; // Chennai Intl Airport (MAA)
    const DEFAULT_COORDS = [13.0827, 80.2707];
    const ANIMATION_SPEED_MS = 1500;

    // --- EXHAUSTIVE GEOGRAPHIC MAPPING FOR ALL 97 COMMANDS ---
    const LOCATION_COORDINATES = {
        'gandhi nagar': [13.007, 80.249], 'cuddalore': [11.75, 79.77], 'velachery': [12.978, 80.221],
        'marina beach': [13.05, 80.28], 'ennore': [13.21, 80.32], 'central railway station': [13.082, 80.275],
        'nagapattinam': [10.76, 79.84], 'metturg dam': [11.79, 77.80], 'metturd dam': [11.79, 77.80], 'mettur dam': [11.79, 77.80],
        'kalpakkam': [12.56, 80.17], 'nilgiris': [11.41, 76.73], 't.nagar': [13.03, 80.23], 'tambaram': [12.92, 80.11],
        'mylapore': [13.03, 80.27], 'pamban bridge': [9.28, 79.20], 'sathyamangalam': [11.50, 77.24],
        'kudankulam': [8.16, 77.71], 'neyveli': [11.60, 79.48], 'rameswaram': [9.28, 79.31],
        'sriperumbudur': [12.96, 79.94], 'ranipet': [12.93, 79.33], 'manali': [13.15, 80.27],
        'ambattur': [13.11, 80.16], 'hosur': [12.74, 77.82], 'ooty': [11.41, 76.70], 'vellore': [12.91, 79.13],
        'karaikal': [10.92, 79.83], 'trichy': [10.79, 78.70], 'tarapur': [19.82, 72.65],
        'ramanathapuram': [9.36, 78.83], 'villupuram': [11.94, 79.49], 'madurai': [9.92, 78.12],
        'thanjavur': [10.78, 79.13], 'avadi': [13.11, 80.10], 'pattukkottai': [10.42, 79.31],
        'coimbatore': [11.01, 76.95], 'korukkupet': [13.12, 80.28], 'poonamallee': [13.05, 80.09],
        'arakkonam': [13.08, 79.67], 'adyar': [13.00, 80.25], 'saidapet': [13.02, 80.22],
        'kilpauk medical college': [13.08, 80.24], 'mudumalai': [11.58, 76.62], 'chennai port': [13.09, 80.29]
    };

    // --- MASSIVE ICON LIBRARY ---
    const ICONS = { commandCenter: L.icon({ iconUrl: 'https://img.icons8.com/color/48/building.png', iconSize: [40, 40] }), defaultUnit: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/26e07f/truck.png', iconSize: [35, 35] }), drone: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/00ddff/drone.png', iconSize: [30, 30] }), amphibious: L.icon({ iconUrl: 'https://img.icons8.com/color/48/airboat.png', iconSize: [40, 40] }), excavator: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/f5a623/excavator.png', iconSize: [35, 35] }), robotArm: L.icon({ iconUrl: 'https://img.icons8.com/external-soft-fill-juicy-fish/60/external-robot-automation-soft-fill-juicy-fish.png', iconSize: [40, 40] }), crawler: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/f5a623/robot-2.png', iconSize: [35, 35] }), snakeRobot: L.icon({ iconUrl: 'https://img.icons8.com/ios/50/00ddff/robot-2.png', iconSize: [35, 35] }), fireRobot: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/e94560/robot-2.png', iconSize: [35, 35] }), deconRobot: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/26e07f/robot-2.png', iconSize: [35, 35] }), printer3d: L.icon({ iconUrl: 'https://img.icons8.com/external-kiranshastry-solid-kiranshastry/64/f5a623/external-3d-printer-industry-kiranshastry-solid-kiranshastry.png', iconSize: [40, 40] }), supplies: L.icon({ iconUrl: 'https://img.icons8.com/plasticine/100/box.png', iconSize: [40, 40] }), fire: L.icon({ iconUrl: 'https://img.icons8.com/color/48/fire-element.png', iconSize: [40, 40] }), hazard: L.icon({ iconUrl: 'https://img.icons8.com/color/48/biohazard.png', iconSize: [40, 40] }), radiation: L.icon({ iconUrl: 'https://img.icons8.com/fluency/48/radiation-warning-sign.png', iconSize: [40, 40] }), ammunition: L.icon({ iconUrl: 'https://img.icons8.com/color/48/missile.png', iconSize: [40, 40] }), medical: L.icon({ iconUrl: 'https://img.icons8.com/color/48/hospital-3.png', iconSize: [35, 35] }), repair: L.icon({ iconUrl: 'https://img.icons8.com/color/48/maintenance.png', iconSize: [35, 35] }), monitor: L.icon({ iconUrl: 'https://img.icons8.com/fluency/48/wifi-router.png', iconSize: [25, 25] }), barrier: L.icon({ iconUrl: 'https://img.icons8.com/color/48/road-closure.png', iconSize: [40, 40] }), power: L.icon({ iconUrl: 'https://img.icons8.com/fluency/48/lightning-bolt.png', iconSize: [35, 35] }), shield: L.icon({ iconUrl: 'https://img.icons8.com/fluency/48/security-shield-green.png', iconSize: [35, 35] }), animal: L.icon({ iconUrl: 'https://img.icons8.com/color/48/pet-commands-summon.png', iconSize: [35, 35] }), data: L.icon({ iconUrl: 'https://img.icons8.com/fluency/48/database.png', iconSize: [35, 35] }), siren: L.icon({ iconUrl: 'https://img.icons8.com/color/48/siren.png', iconSize: [35, 35] }), jammer: L.icon({ iconUrl: 'https://img.icons8.com/ios-filled/50/e94560/no-audio.png', iconSize: [35, 35] }), camera: L.icon({ iconUrl: 'https://img.icons8.com/color/48/camera.png', iconSize: [35, 35] }), };

    // --- MAP & DOM SETUP ---
    const map = L.map('map').setView(DEFAULT_COORDS, 9);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { attribution: '© CARTO & OSM', maxZoom: 20 }).addTo(map);
    L.marker(COMMAND_CENTER_COORDS, { icon: ICONS.commandCenter, title: 'Aura Command Center' }).addTo(map).bindPopup('<b>Aura Command Center</b>');
    const commandInput = document.getElementById('command-input'), processBtn = document.getElementById('process-btn'), parsedOutputSection = document.getElementById('parsed-output'), outputIntent = document.getElementById('output-intent'), outputSafety = document.getElementById('output-safety'), outputParams = document.getElementById('output-params'), commandLog = document.getElementById('command-log'), confirmationDialog = document.getElementById('confirmation-dialog'), confirmBtn = document.getElementById('confirm-btn'), cancelBtn = document.getElementById('cancel-btn'), exampleLink = document.getElementById('example-link');
    let pendingCommand = null, activeLayers = [];
    const logMessage = (msg, type='info') => { const e=document.createElement('div'); e.className=`log-entry log-${type}`; e.textContent=`[${new Date().toLocaleTimeString()}] ${msg}`; commandLog.prepend(e); };

    // --- NLP & ACTION HANDLING ---
    async function processCommand() {
        const text = commandInput.value.trim();
        if (!text) return;
        logMessage(`Processing command: "${text}"`);
        parsedOutputSection.classList.add('hidden');
        clearMap();
        try {
            const response = await fetch('/process_command', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: text }) });
            if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
            const data = await response.json();
            displayParsedOutput(data);
            if (data.confirmation_required) {
                pendingCommand = data;
                document.getElementById('confirmation-text').textContent = `Matched command: "${data.english}". This is a safety-critical operation. Please confirm.`;
                confirmationDialog.classList.remove('hidden');
            } else {
                executeAction(data);
            }
        } catch (error) { logMessage(`Error: ${error.message}`, 'critical'); }
    }
    const displayParsedOutput = data => { outputIntent.textContent = data.intent; outputSafety.innerHTML = data.safety_critical ? '<span style="color: #e94560; font-weight: bold;">YES</span>' : 'No'; outputParams.textContent = JSON.stringify(data.parameters, null, 2); parsedOutputSection.classList.remove('hidden'); };

    // --- VISUALIZATION & ANIMATION ENGINE ---
    function executeAction(commandData) {
        logMessage(`Executing: ${commandData.intent} (based on "${commandData.english}")`, 'success');
        const targetCoords = getCoordinatesFromParams(commandData.parameters);
        map.flyTo(targetCoords, 14, { duration: 1.5 });
        
        const vizProfile = commandData.visualization;
        visualizeEnvironment(vizProfile.environment, targetCoords);
        
        const actionCallback = () => visualizeAction(vizProfile, targetCoords, commandData.parameters);
        
        if (vizProfile.no_unit) {
            actionCallback();
        } else {
            const unitIcon = ICONS[vizProfile.icon] || ICONS.defaultUnit;
            animateMovement(COMMAND_CENTER_COORDS, targetCoords, unitIcon, actionCallback);
        }
    }

    // --- DATA-DRIVEN VISUALIZATION ROUTER ---
    function visualizeAction(viz, coords, params) {
        switch (viz.type) {
            case 'sweep':
                logMessage('Commencing scan.', 'info');
                activeLayers.push(L.marker(coords, { icon: L.divIcon({ className: 'radar-sweep-container', html: `<div class="radar-sweep" style="background: radial-gradient(circle at center, rgba(0, 221, 255, 0) 0%, ${viz.color}20 70%);"></div>` }) }).addTo(map));
                break;
            case 'deploy_supply':
                logMessage('Deploying supplies.', 'info');
                const m = L.marker(coords, { icon: ICONS.supplies, title: '' }).addTo(map);
                m.bindPopup(`<b>Supply Drop</b><br>${params.quantity || ''} ${params.supply_type || 'kits'}`).openPopup();
                activeLayers.push(m);
                break;
            case 'containment':
                logMessage('Establishing perimeter.', 'info');
                const r = parseRadius(params.radius || params.exclusion_zone || params.evacuation_radius || '500m');
                const i = ICONS[viz.hazard_icon] || ICONS.hazard;
                activeLayers.push(L.marker(coords, { icon: i, title: '' }).addTo(map));
                const z = L.circle(coords, { radius: r, color: viz.color, fillColor: viz.color, fillOpacity: 0.2, weight: 2, dashArray: '5, 5' }).addTo(map);
                z.bindPopup(`<b>Hazard Zone</b><br>Radius: ${r}m`).openPopup();
                activeLayers.push(z);
                break;
            case 'path_clearance':
                logMessage('Starting clearance operation.', 'info');
                activeLayers.push(L.marker(coords, { icon: ICONS.excavator, title: '' }).addTo(map));
                const path = L.polyline([coords, [coords[0] + 0.01, coords[1] + 0.01]], { color: '#ff5555', weight: 5, dashArray: '10, 10', className: viz.path_type === 'rail' ? 'path-rail' : '' }).addTo(map);
                const cleared = L.polyline([coords], { color: '#26e07f', weight: 5, className: viz.path_type === 'rail' ? 'path-rail' : '' }).addTo(map);
                activeLayers.push(path, cleared);
                let idx = 0;
                const interval = setInterval(() => { if (idx > 100) { clearInterval(interval); return; } cleared.addLatLng([coords[0] + 0.01 * (idx / 100), coords[1] + 0.01 * (idx / 100)]); idx++; }, 30);
                break;
            case 'path_repair':
                logMessage(`Beginning repairs on ${viz.path_type}.`, 'info');
                const repairType = params.technology?.includes('welders') ? 'weld' : 'generic';
                const animClass = repairType === 'weld' ? 'repair-spark-effect' : 'build-up-effect';
                activeLayers.push(L.marker(coords, { icon: ICONS.repair, title: '' }).addTo(map), L.circle(coords, { radius: 10, color: 'transparent', fillColor: '#FFD700', fillOpacity: 0.8, className: animClass }).addTo(map));
                break;
            case 'deploy_static':
                logMessage(`Deploying static asset: ${viz.deploy_icon}.`, 'info');
                const count = viz.count || 1;
                for (let i = 0; i < count; i++) {
                    const offset = (Math.random() - 0.5) * (0.001 * count);
                    activeLayers.push(L.marker([coords[0] + offset, coords[1] + offset], { icon: ICONS[viz.deploy_icon], title: '' }).addTo(map));
                }
                break;
            case 'point_effect':
                logMessage(`Initiating action: ${viz.effect}`, 'info');
                const effectFunc = getPointEffect(viz.effect);
                if(effectFunc) effectFunc(coords, viz);
                break;
            case 'data_flow':
                logMessage('Initiating data transfer.', 'info');
                const from = L.marker(coords, { icon: ICONS.data, title: '' }).addTo(map);
                const to = L.marker(COMMAND_CENTER_COORDS, { icon: ICONS.commandCenter, title: '' }).addTo(map);
                activeLayers.push(from, to, L.polyline([coords, COMMAND_CENTER_COORDS], { color: '#00ddff', weight: 2, className: 'data-flow-line' }).addTo(map));
                break;
            case 'evacuation_route':
                logMessage('Guiding evacuation.', 'info');
                const sC=[coords[0]+0.02,coords[1]+0.02];
                const s=L.marker(sC,{icon:ICONS.medical, title:''}).addTo(map).bindPopup('<b>Evacuation Shelter</b>');
                activeLayers.push(s, L.polyline([coords,sC],{color:'#26e07f',dashArray:'10, 10',weight:3}).addTo(map));
                break;
            default:
                logMessage(`Unknown visualization type: ${viz.type}`, 'critical');
        }
    }
    
    function getPointEffect(effect) {
        const effects = {
            'power_grid': (coords, viz) => { for(let i=0;i<5;i++){const oLat=(Math.random()-0.5)*0.02,oLng=(Math.random()-0.5)*0.02; const n=L.marker([coords[0]+oLat,coords[1]+oLng],{icon:ICONS.power,title:''}).addTo(map);n.getElement().classList.add('power-node-off');setTimeout(()=>n.getElement().classList.remove('power-node-off'),Math.random()*2000);activeLayers.push(n);}},
            'monitoring': (coords, viz) => { for(let i=0;i<3;i++){const o=(Math.random()-0.5)*0.002; const m=L.marker([coords[0]+o,coords[1]+o],{icon:ICONS.monitor,title:''}).addTo(map); const pulse=L.circle([coords[0]+o,coords[1]+o],{radius:50,color:viz.color,fill:false,className:'monitor-pulse'}).addTo(map); activeLayers.push(m,pulse);}},
            'broadcast': (coords, viz) => { const s=L.marker(coords,{icon:ICONS.siren,title:''}).addTo(map); const w=L.circle(coords,{radius:10,className:'broadcast-wave', style:`box-shadow: 0 0 0 2px ${viz.color}80`}).addTo(map); activeLayers.push(s,w);},
            'jammer': (coords, viz) => { const j=L.marker(coords,{icon:ICONS.jammer,title:''}).addTo(map); const w=L.circle(coords,{radius:10,className:'jammer-wave'}).addTo(map); activeLayers.push(j,w);},
            'decontamination': (coords, viz) => { activeLayers.push(L.marker(coords,{icon:ICONS.radiation,title:''}).addTo(map)); const w=L.circle(coords,{radius:10,className:'cleanse-wave', style:`box-shadow: 0 0 0 3px ${viz.color}80`}).addTo(map); activeLayers.push(w);},
            'debris_sorting': (coords, viz) => { activeLayers.push(L.marker(coords,{icon:ICONS.robotArm,title:''}).addTo(map)); for(let i=0;i<4;i++){const p=L.circle(coords,{radius:10,className:'sort-pulse'}).addTo(map);setTimeout(()=>map.removeLayer(p),2000);}},
            'facial_recognition': (coords, viz) => { for(let i=0;i<4;i++){const oLat=(Math.random()-0.5)*0.03,oLng=(Math.random()-0.5)*0.03; activeLayers.push(L.marker([coords[0]+oLat,coords[1]+oLng],{icon:ICONS.camera,title:''}).addTo(map));}},
            'tunnel_scan': (coords, viz) => { const p=L.circle(coords,{radius:20,color:'#00ddff',fill:false,className:'monitor-pulse'}).addTo(map); activeLayers.push(p);},
            'firefighting': (coords, viz) => { activeLayers.push(L.marker(coords,{icon:ICONS.fire,title:''}).addTo(map));},
            'water_bombing': (coords, viz) => { for(let i=0;i<3;i++){setTimeout(()=>{const d=L.circle(coords,{radius:10,color:'blue',className:'water-drop-effect'}).addTo(map);setTimeout(()=>map.removeLayer(d),2000);},i*1000);}},
            'shield': (coords, viz) => {const s=L.marker(coords,{icon:ICONS.shield,title:''}).addTo(map); const pulse=L.circle(coords,{radius:100,color:'#26e07f',fill:false,className:'monitor-pulse'}).addTo(map);activeLayers.push(s,pulse);},
            'demolition': (coords, viz) => {const d=L.circle(coords,{radius:10,className:'demolition-effect'}).addTo(map);activeLayers.push(d);setTimeout(()=>map.removeLayer(d),1500);}
        };
        return effects[effect];
    }

    // --- HELPER FUNCTIONS ---
    const visualizeEnvironment = (env, coords) => { if(!env) return; if(env.includes('rubble') || env.includes('derailment') || env.includes('earthquake')) activeLayers.push(L.geoJSON(createRubbleGeoJSON(coords, 200), { style: { color: "#666", weight: 1, fillColor: "#555", fillOpacity: 0.6 } }).addTo(map)); if(env.includes('water') || env.includes('flood')) activeLayers.push(L.circle(coords, { radius: 1000, color: '#0077be', fillColor: '#0077be', fillOpacity: 0.3, weight: 1 }).addTo(map)); if(env.includes('fire')) activeLayers.push(L.circle(coords, { radius: env.includes('forest') ? 1500 : 500, color: '#a52a2a', fillColor: '#8b0000', fillOpacity: 0.4 }).addTo(map)); };
    const isUnitRequired = (cmd) => !cmd.visualization.no_unit;
    function animateMovement(start,end,icon,onComplete){const unit=L.marker(start,{icon:icon,zIndexOffset:1000, title: ''}).addTo(map);let i=0;const steps=100,latStep=(end[0]-start[0])/steps,lngStep=(end[1]-start[1])/steps;const interval=setInterval(()=>{if(i>=steps){clearInterval(interval);map.removeLayer(unit);if(onComplete)onComplete();return;}unit.setLatLng([start[0]+latStep*i,start[1]+lngStep*i]);i++;},ANIMATION_SPEED_MS/steps);}
    const getUnitIcon = (cmd) => ICONS[cmd.visualization.icon] || ICONS.defaultUnit;
    function getCoordinatesFromParams(params){if(params.coordinates){const p=parseCoordinates(params.coordinates);if(p)return p;}if(params.location){const loc=params.location.toLowerCase();for(const[name,coords]of Object.entries(LOCATION_COORDINATES)){if(loc.includes(name.split(' ')[0]))return coords;}}return DEFAULT_COORDS;}
    function clearMap(){activeLayers.forEach(layer=>map.removeLayer(layer));activeLayers=[];}
    const parseCoordinates=(str)=>{if(!str)return null;const m=str.match(/(\d+\.?\d*)\D*([NS])\D*(\d+\.?\d*)\D*([EW])/);return m?[m[2]==='N'?m[1]:-m[1],m[4]==='E'?m[3]:-m[3]]:null;};
    const parseRadius=(str)=>{if(!str)return 500;const v=parseFloat(str);return str.toLowerCase().includes('km')?v*1000:v;};
    const createRubbleGeoJSON=(c,r)=>{const p=15,cs=[];for(let i=0;i<p;i++){const a=(i/p)*2*Math.PI,d=(r/111320)*(0.7+Math.random()*0.3);cs.push([c[1]+Math.cos(a)*d,c[0]+Math.sin(a)*d]);}cs.push(cs[0]);return{"type":"Polygon","coordinates":[cs]};};
    async function fetchAndSetExample(){try{const r=await fetch('/process_command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:'get_example'})});const e=await r.json();if(e.english){exampleLink.textContent=`"${e.english}"`;exampleLink.onclick=(ev)=>{ev.preventDefault();commandInput.value=e.english;fetchAndSetExample();};}}catch(err){console.error(err);}}
    
    // --- EVENT LISTENERS ---
    processBtn.addEventListener('click', processCommand); commandInput.addEventListener('keydown',(e)=>e.key==='Enter'&&processCommand()); confirmBtn.addEventListener('click',()=>{if(pendingCommand)executeAction(pendingCommand);confirmationDialog.classList.add('hidden');pendingCommand=null;}); cancelBtn.addEventListener('click',()=>{logMessage(`Action cancelled by operator: ${pendingCommand?.intent}`,'info');confirmationDialog.classList.add('hidden');pendingCommand=null;});
    fetchAndSetExample();
});