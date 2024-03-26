

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(on b c)
(ontable c)
(on d a)
(on e d)
(clear e)
)
(:goal
(and
(on a b)
(on d c)
(on e d))
)
)


