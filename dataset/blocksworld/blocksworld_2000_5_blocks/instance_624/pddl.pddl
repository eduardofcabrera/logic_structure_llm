

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(ontable c)
(on d a)
(on e b)
(clear e)
)
(:goal
(and
(on a c)
(on c d)
(on e a))
)
)


