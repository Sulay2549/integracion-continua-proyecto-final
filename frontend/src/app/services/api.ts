import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class Api {
  private backendUrl = 'http://localhost:5000';

  constructor(private http: HttpClient) {}

  validarConexion(): Observable<any> {
    return this.http.get(`${this.backendUrl}/`);
  }
}
