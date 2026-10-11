import { zodResolver } from '@hookform/resolvers/zod'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { z } from 'zod'
import { useAuth } from './AuthProvider'

const credentialsSchema = z.object({
  email: z.string().trim().email('Enter a valid email address.'),
  password: z.string().min(1, 'Enter your password.'),
})

type Credentials = z.infer<typeof credentialsSchema>

export function SignInForm() {
  const { signIn } = useAuth()
  const [requestError, setRequestError] = useState('')
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<Credentials>({
    resolver: zodResolver(credentialsSchema),
  })

  const submit = async ({ email, password }: Credentials) => {
    setRequestError('')
    try {
      await signIn(email, password)
    } catch (error) {
      setRequestError(error instanceof Error ? error.message : 'Sign-in failed. Try again.')
    }
  }

  return (
    <form className="sign-in-form" onSubmit={handleSubmit(submit)} noValidate>
      <div className="form-field">
        <label htmlFor="email">Work email</label>
        <input
          id="email"
          type="email"
          autoComplete="username"
          autoCapitalize="none"
          inputMode="email"
          aria-invalid={Boolean(errors.email)}
          aria-describedby={errors.email ? 'email-error' : undefined}
          {...register('email')}
        />
        {errors.email && <p className="field-error" id="email-error">{errors.email.message}</p>}
      </div>
      <div className="form-field">
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          aria-invalid={Boolean(errors.password)}
          aria-describedby={errors.password ? 'password-error' : undefined}
          {...register('password')}
        />
        {errors.password && <p className="field-error" id="password-error">{errors.password.message}</p>}
      </div>
      {requestError && <p className="form-error" role="alert">{requestError}</p>}
      <button className="sign-in-button" type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Checking credentials…' : 'Sign in'}
      </button>
    </form>
  )
}
