import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Api } from './services/api';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  title = 'Sistema de Gestión de Tareas';
  mensaje = '';

  constructor(private api: Api) {}

  validarBackend() {
    this.api.validarConexion().subscribe({
      next: (res) => this.mensaje = 'Backend responde correctamente',
      error: (err) => this.mensaje = 'Error al conectar con el backend'
    });
  }
}
