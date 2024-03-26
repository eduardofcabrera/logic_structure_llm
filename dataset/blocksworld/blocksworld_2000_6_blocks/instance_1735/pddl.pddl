

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(ontable c)
(on d c)
(on e d)
(clear b)
(clear e)
)
(:goal
(and
(on a e)
(on b c)
(on e b))
)
)


