import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Api {
  // Construir URL dinámicamente basada en el host actual
  private backendUrl = `http://${window.location.hostname}:5000`;

  constructor(private http: HttpClient) {}

  validarConexion(): Observable<any> {
    return this.http.get(`${this.backendUrl}/`);
  }
}
