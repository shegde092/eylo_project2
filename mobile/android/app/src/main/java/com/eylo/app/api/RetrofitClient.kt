package com.eylo.app.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    // 10.0.2.2 is localhost for Android Emulator
    private const val BASE_URL = "http://10.0.2.2:8000"

    val instance: EyloService by lazy {
        val retrofit = Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        retrofit.create(EyloService::class.java)
    }
}
