

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(ontable c)
(ontable d)
(on e d)
(clear b)
(clear e)
)
(:goal
(and
(on a b)
(on d a)
(on e c))
)
)


