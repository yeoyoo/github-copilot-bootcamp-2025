# Spring Boot 기반 자바 개발을 위한 코드 생성 가이드 (VSCode + GitHub Copilot)

이 문서는 VSCode에서 GitHub Copilot을 활용해 Spring Boot 기반 자바 프로젝트를 개발할 때 따를 코드 생성 규칙과 가이드를 정의합니다.

---

## 1. 기본 설정

- **사용 언어**: Java 17 이상
- **프레임워크**: Spring Boot 3.x
- **빌드 도구**: Gradle (Kotlin DSL) 또는 Maven
- **프로젝트 구조**: `src/main/java`, `src/main/resources` 표준 구조 사용
- **이름 규칙**: 클래스 및 메서드는 `CamelCase`, 변수는 `lowerCamelCase`

---

## 2. 패키지 구조 예시

```
com.example.project
├── controller    // REST 컨트롤러
├── service       // 비즈니스 로직
├── repository    // JPA 레포지토리
├── domain        // 엔티티 및 도메인 모델
├── dto           // DTO (데이터 전송 객체)
├── config        // 설정 클래스
├── exception     // 커스텀 예외 및 핸들러
```

---

## 3. 코드 스타일

- **생성자 주입** 사용 (`@RequiredArgsConstructor`)
- **Lombok**으로 보일러플레이트 제거:
  - `@Getter`, `@Setter`, `@ToString`, `@NoArgsConstructor`, `@AllArgsConstructor`
- 모든 **public 클래스 및 메서드에 JavaDoc** 작성
- 로그는 `@Slf4j`로 처리

---

## 4. REST API 작성 규칙

- `@RestController`, `@RequestMapping` 사용
- 응답은 `ResponseEntity<>`로 감싸기
- 요청 바디 검증은 `@Valid`와 함께 `@RequestBody` 사용
- 예외는 `@ControllerAdvice`로 전역 처리

---

## 5. JPA 작성 규칙

- `@Entity`, `@Table`, `@Id` 필수 사용
- `@ManyToOne(fetch = FetchType.LAZY)` 선호
- 양방향 매핑은 꼭 필요할 때만 사용
- 엔티티는 직접 반환하지 말고 DTO를 사용

---

## 6. 테스트 작성 규칙

- 통합 테스트: `@SpringBootTest`, 컨트롤러 테스트: `@WebMvcTest`
- 의존성 목킹: `@MockBean` 또는 `Mockito`
- 테스트 클래스 이름: `클래스명 + Test.java`
- 테스트는 `src/test/java` 아래에 위치

---

## 7. Copilot 활용 팁

- `// 생성: 설명` 형태의 주석으로 Copilot에게 명령
- 메서드 시그니처나 클래스 선언만 먼저 작성해도 자동 완성 유도 가능
- 생성된 코드는 반드시 **리팩토링 및 검토**할 것
- 필요한 로직 흐름에 대해 인라인 주석 사용 (예: `// 사용자 존재 여부 확인`)

---

## 예시 프롬프트

```java
// 생성: 사용자(User) 엔티티를 관리하는 REST 컨트롤러
```

```java
// 생성: 이메일로 사용자 조회하는 서비스 메서드
```

---

## 8. 의존성 설정 예시 (Gradle Kotlin DSL 기준)

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jpa")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("org.projectlombok:lombok")
    runtimeOnly("com.h2database:h2") // 또는 사용 중인 DBMS
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}
```

---

## 9. API 문서화

- Swagger(OpenAPI) 문서를 위해 `springdoc-openapi` 사용
- 컨트롤러에 `@Operation`, DTO나 엔티티에 `@Schema` 활용

---

**끝.**
