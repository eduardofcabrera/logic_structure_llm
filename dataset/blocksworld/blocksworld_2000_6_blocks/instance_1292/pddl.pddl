

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(on c a)
(ontable d)
(on e d)
(clear b)
)
(:goal
(and
(on a c)
(on c b)
(on d a))
)
)


